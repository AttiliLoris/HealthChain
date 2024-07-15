from collections import namedtuple

from web3 import Web3

from offChain.model.model import Model

CaregiverData = namedtuple('CaregiverData', ['name', 'surname'])
class Caregiver(Model):
    def __init__(self, provider_url):
        super().__init__(provider_url,'caregiver')

    def create_caregiver(self, account, private_key, name, surname,cf):
        transaction = self.contract.functions.registerCaregiver(name, surname, cf).build_transaction({
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
        transaction = self.contract.functions.updateCaregiver(name,surname).build_transaction({
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