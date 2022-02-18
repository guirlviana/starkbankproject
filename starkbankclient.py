import starkbank
from credentials import PRIVATE_KEY, PROJECT_ID
from datetime import datetime, timedelta
import random


class StarkBankClient():
    date_today = datetime.now().strftime('%Y-%m-%d')

    def __init__(self): # authenticate the client and the project
        project = starkbank.Project(
            environment="sandbox",
            id=PROJECT_ID, # your project id
            private_key=PRIVATE_KEY # your private key
        )

        starkbank.user = project
        starkbank.language = 'pt-BR'
        self.credited_invoices_list = list() # daily id invoices history
    
    def issue_invoice(self, amount_to_send, tax_id, name):
        '''
            send invoices.

                    Parameters:
                            amount_to_send (int): A decimal integer
                            tax_id (str): Payer CPF or CNPJ
                            name (str): Payer full name
        '''
        try:
            starkbank.invoice.create([starkbank.Invoice(amount=amount_to_send, tax_id=tax_id, name=name)])
        
        except Exception as e:
            print("An unexpected error has occurred: ", e)
        
        else:
            print(f"{name} invoice issued")


    def listen_webhook(self, last_hour=3):
        '''
            Listener webhook method

                    Parameters:
                            last_hour (int): Last hour to set the interval of invoices (default is 3)
                            
        '''
        events = starkbank.event.query(
            after=self.date_today,
            before=self.date_today,  
        )

        time_now = datetime.now()
        last_hour_ago = time_now - timedelta(hours=last_hour)
        
        for event in events:
            if event.log.type == "credited":
                
                invoice_date = event.log.invoice.updated - timedelta(hours=3) # Convert UTC Time to local time
                invoice_id = event.log.invoice.id

                if invoice_date >= last_hour_ago and invoice_date <= time_now: # transfer invoices at interval (now - last_hour)
                
                    if invoice_id not in self.credited_invoices_list: # if invoice id not in credited invoices list, transfer and add to list
                        
                        self.create_transfer((event.log.invoice.amount))
                        self.credited_invoices_list.append(invoice_id) # append invoice id to avoid duplicate 
                
                else: # if invoice_date is not at interval and in credited invoices list
                    if invoice_id in self.credited_invoices_list:
                        
                        self.credited_invoices_list.remove(invoice_id)


    def create_transfer(self, invoice_amount):
        '''
           create a transfer 

                    Parameters:
                            invoice_amount (int): Amount of invoice
        '''

        # generate external id for each transfer
        external_id = f'external-id-{random.randint(100, 999)}{random.randint(100, 999)}{random.randint(100, 999)}'
        transfers = starkbank.transfer.create([
            starkbank.Transfer(
                amount=invoice_amount,
                tax_id="20.018.183/0001-80",
                name="Stark Bank S.A.",
                bank_code="20018183",
                branch_code="0001",
                account_number="6341320293482496",
                account_type='payment',
                external_id= external_id
            )
        ])
        for transfer in transfers:
            if transfer.status == 'created':
                print('Transfer made successfully')

    def create_webhook(self, url, subscriptions):
        '''
            create a webhook

                    Parameters:
                            url (string): Webhook url
                            subscriptions (list): list of subscriptions methods example ["invoice"]
        '''
        try:
            webhook = starkbank.webhook.create(
                url=url,
                subscriptions=subscriptions,
            )
        except Exception as e:
            print("An unexpected error has occurred: ", e)
        
        else:
            if webhook.id:
                print(f"Webhook subscriptions {subscriptions} created at ", self.date_today)
   