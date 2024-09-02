import json

from web3 import Web3
from eth_account import Account
from .model import Model


class PatientData:
    def __init__(self, name, lastname,birthPlace, password, isRegistered, isIndependent, cf):
        self.name = name
        self.lastname = lastname
        self.birthPlace = birthPlace
        self.password = password
        self.isRegistered = isRegistered
        self.isIndependent = isIndependent
        self.cf = cf


class Patient(Model):
    def __init__(self, provider_url, conn):
        super().__init__(provider_url, 'patient', conn)

    def create_patient(self, name, lastname, birthPlace, pwd, isIndependent,cf):
        address, private_key = super().create_new_account()

        transaction = self.contract.functions.registerPatient(name, lastname, birthPlace, pwd, isIndependent,cf,address,private_key).build_transaction({
            'from': address,
            'nonce': self.web3.eth.get_transaction_count(address),
            'gas': 2000000,
            'gasPrice': self.web3.to_wei('0', 'gwei')
        })

        signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key=private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def update_patient(self, name, lastname, birthPlace, pwd, isIndependent,cf):
        data = super().cf_to_address(cf)
        transaction = self.contract.functions.updatePatient(name, lastname, birthPlace, pwd, isIndependent,cf).build_transaction({
            'from': data['address'],
            'nonce': self.web3.eth.get_transaction_count(data['address']),
            'gas': 2000000,
            'gasPrice': self.web3.to_wei('0', 'gwei')
        })

        signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key=data['private_key'])
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def get_patient(self,cf):
        data = super().cf_to_address(cf)
        if data:
            name, lastname, birthPlace, pwd, isIndependent, cf = self.contract.functions.getPatient(cf).call({'from': data['address']})
            patient = PatientData(name, lastname, birthPlace, pwd, 1,isIndependent,cf)
            return patient
        return 0

