from starkbankclient import StarkBankClient

client = StarkBankClient()
client.issue_invoice(amount_to_send=15, tax_id='560.610.660-40', name='Carlos Eduardo')
# my_invoices = client.get_invoices(limit=12)
# client.transfer_invoices(my_invoices, 1)