from collections import namedtuple

from web3 import Web3

from .model import Model

class CaregiverData:
    def __init__(self, name, lastname, password, isRegistered, cf):
        self.name = name
        self.lastname = lastname
        self.password = password
        self.isRegistered = isRegistered
        self.cf = cf
class Caregiver(Model):
    def __init__(self, provider_url):
        super().__init__(provider_url,'caregiver')

    def create_caregiver(self, account, private_key, name, lastname, hashedPwd, cf):
        transaction = self.contract.functions.registerCaregiver(name, lastname, hashedPwd, cf).build_transaction({
            'from': account,
            'nonce': self.web3.eth.get_transaction_count(account),
            'gas': 2000000,
            'gasPrice': self.web3.to_wei('50', 'gwei')
        })

        signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key=private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def update_caregiver(self, cf, private_key, name, lastname):
        transaction = self.contract.functions.updateCaregiver(name,lastname, cf).build_transaction({
            'from': cf,
            'nonce': self.web3.eth.get_transaction_count(cf),
            'gas': 2000000,
            'gasPrice': self.web3.to_wei('50', 'gwei')
        })

        signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key=private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_teceipt(tx_hash)
        return receipt

    def get_caregiver(self, cf):
        name, lastname,pwd, cf= self.contract.functions.getCaregiver(cf).call({'from': '0x098049451CC663e32544Bb4AA2136df812b5235c'})
        caregiver = CaregiverData(name, lastname,pwd, 0, cf)
        if caregiver.name:
            caregiver.isRegistered = True
        return caregiver