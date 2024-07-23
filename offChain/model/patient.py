import json
from collections import namedtuple

from web3 import Web3
from eth_account import Account
from .model import Model

PatientData = namedtuple('PatientData', ['name', 'lastname', 'birthPlace','password','isRegistered','isIndependent','cf'])
class Patient(Model):
    def __init__(self, provider_url):
        super().__init__(provider_url, 'patient')

    def create_patient(self, private_key, name, lastname, birthPlace, pwd, isIndependent,cf):
        address, private_key = self.create_new_account()

        transaction = self.contract.functions.registerPatient(name, lastname, birthPlace, pwd, isIndependent,cf).build_transaction({
            'from': address,
            'nonce': self.web3.eth.get_transaction_count(address),
            'gas': 2000000,
            'gasPrice': self.web3.to_wei('50', 'gwei')
        })

        signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key=private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def update_patient(self, account, private_key, name, lastname, birthPlace, pwd, isIndependent,cf):
        transaction = self.contract.functions.updatePatient(name, lastname, birthPlace, pwd, isIndependent,cf).build_transaction({
            'from': account,
            'nonce': self.web3.eth.get_transaction_count(account),
            'gas': 2000000,
            'gasPrice': self.web3.to_wei('50', 'gwei')
        })

        signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key=private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def get_patient(self,cf):
        name, lastname, birthPlace, pwd, isIndependent, cf = self.contract.functions.getPatient(cf).call({'from': '0x098049451CC663e32544Bb4AA2136df812b5235c'})
        patient = PatientData(name, lastname, birthPlace, pwd, 1,isIndependent,cf)
        return patient

    def create_new_account(self):
        # Genera un nuovo account
        new_account = Account.create()

        # Estrai l'indirizzo e la chiave privata
        address = new_account.address
        private_key = new_account.privateKey.hex()

        return address, private_key