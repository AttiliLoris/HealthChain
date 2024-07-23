import json
from collections import namedtuple
from web3 import Web3

from .model import Model

class DoctorData:
    def __init__(self, name, lastname, password, isRegistered, cf):
        self.name = name
        self.lastname = lastname
        self.password = password
        self.isRegistered = isRegistered
        self.cf = cf
class Doctor(Model):
    def __init__(self, provider_url):
        super().__init__(provider_url,'doctor')

    def create_doctor(self,name, lastname, hashedPwd, cf):
        address, private_key = super().create_new_account()
        transaction = self.contract.functions.createDoctor(name, lastname, hashedPwd, cf).build_transaction({
            'from': address,
            'nonce': self.web3.eth.get_transaction_count(private_key),
            'gas': 2000000,
            'gasPrice': self.web3.to_wei('50', 'gwei')
        })

        signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key=private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def update_doctor(self, cf,  name, lastname):
        data = super().cf_to_address(cf)
        transaction = self.contract.functions.updateDoctor( name, lastname,cf).build_transaction({
            'from': data['address'],
            'nonce': self.web3.eth.get_transaction_count(data['address']),
            'gas': 2000000,
            'gasPrice': self.web3.to_wei('50', 'gwei')
        })

        signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key=data['private_key'])
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.wait_for_Transaction_receipt(tx_hash)
        return receipt

    def get_doctor(self, cf):
        data=super().cf_to_address(cf)
        name, lastname,pwd, cf= self.contract.functions.getDoctor(cf).call({'from': str(data['address'])})
        doctor = DoctorData(name, lastname,pwd,0, cf)
        if doctor.name:
            doctor.isRegistered=True
        return doctor

