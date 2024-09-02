import time
from collections import namedtuple

from web3 import Web3

from .model import Model


class HealthFileData:
    def __init__(self, cf, clinicalHistory, prescriptions, treatmentPlan, notes):
        self.cf = cf
        self.clinicalHistory = clinicalHistory
        self.prescriptions = prescriptions
        self.prescriptions = prescriptions
        self.treatmentPlan = treatmentPlan
        self.notes = notes

class HealthFile(Model):
    def __init__(self, provider_url):
        super().__init__(provider_url,'healthFile')

    def create_healthFile(self, cf):
        time.sleep(3)
        data = super().cf_to_address(cf)
        transaction = self.contract.functions.createEmptyHealthFile(cf).build_transaction({
            'from': data['address'],
            'nonce': self.web3.eth.get_transaction_count(data['address']),
            'gas': 2000000,
            'gasPrice': self.web3.to_wei('0', 'gwei')
        })

        signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key=data['private_key'])
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def update_healthFile(self, cf,clinicalHistory,prescriptions,treatmentPlan,notes):

        data = super().cf_to_address(cf)
        transaction = self.contract.functions.updateHealthFile(cf,clinicalHistory,prescriptions,treatmentPlan,notes).build_transaction({
            'from': data['address'],
            'nonce': self.web3.eth.get_transaction_count(data['address']),
            'gas': 2000000,
            'gasPrice': self.web3.to_wei('0', 'gwei')
        })

        signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key=data['private_key'])
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def get_healthFile(self, cf):
        data = super().cf_to_address(cf)
        if data:
            cf,clinicalHistory,prescriptions,treatmentPlan,notes = self.contract.functions.getHealthFile(cf).call({'from': data['address']})
            healthFile = HealthFileData(cf,clinicalHistory,prescriptions,treatmentPlan,notes)
            return healthFile
        return None

    def confirm_treatment(self, cfCaregiver, cfPatient, isIndependent):
        if isIndependent:
            data = super().cf_to_address(cfPatient)
            transaction = self.contract.functions.confirmTreatment(cfCaregiver,cfPatient).build_transaction({
                'from': data['address'],
                'nonce': self.web3.eth.get_transaction_count(data['address']),
                'gas': 2000000,
                'gasPrice': self.web3.to_wei('0', 'gwei')
            })
        else:
            data = super().cf_to_address(cfCaregiver)
            transaction = self.contract.functions.confirmTreatment(cfCaregiver, cfPatient).build_transaction({
                'from': data['address'],
                'nonce': self.web3.eth.get_transaction_count(data['address']),
                'gas': 2000000,
                'gasPrice': self.web3.to_wei('0', 'gwei')
            })

        signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key=data['private_key'])
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt