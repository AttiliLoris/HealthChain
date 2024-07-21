from collections import namedtuple

from web3 import Web3

from .model import Model

HealthFileData = namedtuple('HealthData', ['cf','clinicalHistory','prescriptions','treatmentPlan','notes'])
class HealthFile(Model):
    def __init__(self, provider_url):
        super().__init__(provider_url,'healthFile')

    def create_healthFile(self, private_key, cf):
        transaction = self.contract.functions.createEmptyHealthFile(cf).build_transaction({
            'from': '0x098049451CC663e32544Bb4AA2136df812b5235c',
            'nonce': self.web3.eth.get_transaction_count('0x098049451CC663e32544Bb4AA2136df812b5235c'),
            'gas': 2000000,
            'gasPrice': self.web3.to_wei('50', 'gwei')
        })

        signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key=private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def update_healthFile(self,private_key, cf,clinicalHistory,prescriptions,treatmentPlan,note):
        transaction = self.contract.functions.updatehealthFile(cf,clinicalHistory,prescriptions,treatmentPlan,note).build_transaction({
            'from': cf,
            'nonce': self.web3.eth.getTransactionCount(cf),
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei')
        })

        signed_txn = self.web3.eth.account.signTransaction(transaction, private_key=private_key)
        tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        return receipt

    def get_healthFile(self, cf):
        cf,clinicalHistory,prescriptions,treatmentPlan,note = self.contract.functions.getHealthFile(cf).call({'from': '0x098049451CC663e32544Bb4AA2136df812b5235c'})
        healthFile = HealthFileData(cf,clinicalHistory,prescriptions,treatmentPlan,note)
        return healthFile
    #isIndependet da fare

    def confirm_treatment(self, cfCaregiver,cfPatient , isIndependent, private_key):
        if isIndependent:
            transaction = self.contract.functions.confirmTreatment(cfCaregiver,cfPatient).build_transaction({
                'from': cfPatient,
                'nonce': self.web3.eth.getTransactionCount(cfPatient),
                'gas': 2000000,
                'gasPrice': self.web3.toWei('50', 'gwei')
            })
        else:
            transaction = self.contract.functions.confirmTreatment(cfCaregiver, cfPatient).build_transaction({
                'from': cfCaregiver,
                'nonce': self.web3.eth.getTransactionCount(cfCaregiver),
                'gas': 2000000,
                'gasPrice': self.web3.toWei('50', 'gwei')
            })

        signed_txn = self.web3.eth.account.signTransaction(transaction, private_key=private_key)
        tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        return receipt