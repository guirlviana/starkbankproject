import starkbank
from credentials import PRIVATE_KEY, PROJECT_ID
from datetime import datetime, timedelta
import random

class StarkBankClient():
    
    def __init__(self): # authenticate the client and the project
        project = starkbank.Project(
            environment="sandbox",
            id=PROJECT_ID, # your project id
            private_key=PRIVATE_KEY # your private key
        )

        starkbank.user = project
        starkbank.language = 'pt-BR'

    
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
            print(f"{name} invoice issued at {datetime.now()}")

    
    def get_invoices(self, limit=12):
        '''
            Returns daily invoices with the status of paid.

            Parameters:
                    limit (int): number of invoices returned, default is 12
                    
            Returns:
                    list of invoices (list)
        '''
        date_today = datetime.now().strftime('%Y-%m-%d')

        return starkbank.invoice.query(after=date_today, before=date_today, limit=limit, status='paid')

    def transfer_invoices(self, invoices, last_hour=3):
        '''
            Transfer invoices 

            Parameters:
                    invoices (list): List of invoices
                    last_hour (int): invoices in time interval (now - last_hour)

        '''
        time_now = datetime.now()
        last_hour_ago = time_now - timedelta(hours=last_hour)

        # create a transfer
        def create_transfer(invoice_amount):
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
            # if transfer is created send a success message to user
            for transfer in transfers:
                if transfer.status == 'created':
                    print('Transfer made successfully')


        for invoice in invoices:
            invoice_date = invoice.created - timedelta(hours=3) # Convert UTC Time to local time

            if invoice_date >= last_hour_ago and invoice_date <= time_now: # transfer invoices at interval (now - last_hour)
                create_transfer(invoice.amount)
