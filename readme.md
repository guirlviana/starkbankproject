# StarkBank Challenge
## Task
1. Issues 8 to 12 Invoices every 3 hours to random people for 24 hours (our Sandbox
emulation environment will make sure some of those are automatically paid);
2. Receives the webhook callback of the Invoice credit and sends the received amount
(minus eventual fees) to the following account using a Transfer

## Files

| Files | Description |
| ------ | ------ |
| Program | Code solution |
| StarkBankClient | Class that interacts with the StarkBank API |
| Requirements | Dependencies of project

## First Step
1- Run the follow code in the root folder to install dependencies
```sh
pip install requirements.txt
```
2- Create a python file as "credentials.py" and insert the code below
`Note: StarkBankClient class will find for credentials file at root folder and PRIVATE_KEY, PROJECT_ID variables`
```sh
PRIVATE_KEY = '''YOUR_PRIVATE_KEY'''
```
```sh
PROJECT_ID = 'YOUR_PROJECT_ID'
```
3- At [program.py](https://github.com/guirlviana/starkbankproject/blob/main/program.py#L28) line 28 | change the url webhook for yours and put your subscriptions, if webhook have already created just keep the line commented to avoid an error
## The solution

Finally, run the program.py
```sh
python program.py
```
All code has comments to help the dev community enjoy.
You can follow the results through the terminal or on your project's dashboard at Stark Bank.


>It was a great challenge and very pleasant to develop. 
Guilherme Viana Dev.

