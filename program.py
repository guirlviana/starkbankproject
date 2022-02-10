from starkbankclient import StarkBankClient
import schedule
import random

def issue_and_transfer_invoices():
    client = StarkBankClient()

    for i in range(0, random.randint(8, 12)):
        invoice_amount = random.randint(100, 1000000)
        client.issue_invoice(amount_to_send=invoice_amount, tax_id='560.610.660-40', name='John Mike')
        
    
    my_invoices = client.get_invoices(limit=12)
    client.transfer_invoices(my_invoices, 3)


if __name__ == '__main__':
    while True:
        schedule.every(3).hours.do(issue_and_transfer_invoices)