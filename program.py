from starkbankclient import StarkBankClient
import schedule
import random


def issue_invoices(client, min_issue=8, max_issue=12):
    number_of_invoices = random.randint(min_issue, max_issue)
    for i in range(0, number_of_invoices):
        invoice_amount = random.randint(100, 1000000)
        client.issue_invoice(amount_to_send=invoice_amount, tax_id='560.610.660-40', name='John Mike')

def transfer_invoices(client):
    my_invoices = client.get_invoices()
    client.transfer_invoices(my_invoices)


if __name__ == '__main__':
    client = StarkBankClient()
    issue_invoices(client)
    transfer_invoices(client)
    # while True:
    #     schedule.every(3).hours.do(issue_and_transfer_invoices)