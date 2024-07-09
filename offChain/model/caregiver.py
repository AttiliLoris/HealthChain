from collections import namedtuple

from web3 import Web3

CaregiverData = namedtuple('CaregiverData', ['name', 'surname'])
class Caregiver:
    def __init__(self, provider_url, contract_address, abi):
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract_address = contract_address
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=abi)

    def create_caregiver(self, account, private_key, name, surname,cf):
        transaction = self.contract.functions.registerCaregiver(name, surname, cf).buildTransaction({
            'from': account,
            'nonce': self.web3.eth.getTransactionCount(account),
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei')
        })

        signed_txn = self.web3.eth.account.signTransaction(transaction, private_key=private_key)
        tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        return receipt

    def update_caregiver(self, account, private_key, name, surname):
        transaction = self.contract.functions.updateCaregiver(name,surname).buildTransaction({
            'from': account,
            'nonce': self.web3.eth.getTransactionCount(account),
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei')
        })

        signed_txn = self.web3.eth.account.signTransaction(transaction, private_key=private_key)
        tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        return receipt

    def get_caregiver(self, account):
        name, surname = self.contract.functions.getCaregiver().call({'from': account})
        caregiver = CaregiverData(name, surname)
        return caregiver