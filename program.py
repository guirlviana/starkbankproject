from starkbankclient import StarkBankClient
import schedule
import random
import time
from cpf_generator import CPF
from faker import Faker

def issue_invoices(client, min_issue=8, max_issue=12):
    number_of_invoices = random.randint(min_issue, max_issue) # random a value of invoices (8 to 12)
    
    for i in range(0, number_of_invoices):
        invoice_amount = random.randint(100, 1000000) # get a random amount to invoice
        cpf = CPF.generate() # Will generate a random CPF ex: 4606492724
        name = Faker().name() # Will generate a random name ex: Connor Jones
        
        # issue the invoice (change the fake values to yours) default is random
        client.issue_invoice(amount_to_send=invoice_amount, tax_id=cpf, name=name) 





if __name__ == '__main__':

    client = StarkBankClient() # instance a client

        # Run the line below only once
    # client.create_webhook("https://webhook.site/e8555c1f-91ff-4255-9b1c-736d7c5ece5e", ["invoice"])
    
    schedule.every(3).minutes.do(issue_invoices, client)

    # checks the pending and listen webhook every one minute
    while True:
        schedule.run_pending()
        client.listen_webhook()
        time.sleep(60)
    

    
