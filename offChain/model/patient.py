import json
from collections import namedtuple

from web3 import Web3

from offChain.model.model import Model

provider_url = "http://ganache:8080"
PatientData = namedtuple('PatientData', ['name', 'surname', 'cf'])
class Patient(Model):
    def __init__(self, provider_url):
        super().__init__(provider_url, 'patient')

    def create_patient(self, account, private_key, name, surname, cf):
        transaction = self.contract.functions.createPatient(name, surname, cf).build_transaction({
            'from': account,
            'nonce': self.web3.eth.getTransactionCount(account),
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei')
        })

        signed_txn = self.web3.eth.account.signTransaction(transaction, private_key=private_key)
        tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        return receipt

    def update_patient(self, account, private_key, name, surname, cf):
        transaction = self.contract.functions.updatePatient(name, surname, cf).build_transaction({
            'from': account,
            'nonce': self.web3.eth.getTransactionCount(account),
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei')
        })

        signed_txn = self.web3.eth.account.signTransaction(transaction, private_key=private_key)
        tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        return receipt

    def get_patient(self, account):
        name, surname, cf = self.contract.functions.getDoctor().call({'from': account})
        patient = PatientData(name, surname, cf)
        return patient

