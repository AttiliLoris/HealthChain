from collections import namedtuple

from web3 import Web3
provider_url = "http://ganache:8080"
HealthFileData = namedtuple('HealthData', ['name', 'surname', 'cf'])
class HealthFile:
    def __init__(self, provider_url, contract_address, abi):
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract_address = contract_address
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=abi)

    def create_healthFile(self, account, private_key, cf):
        transaction = self.contract.functions.createHealthFile(cf,'','','','').build_transaction({
            'from': account,
            'nonce': self.web3.eth.getTransactionCount(account),
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei')
        })

        signed_txn = self.web3.eth.account.signTransaction(transaction, private_key=private_key)
        tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        return receipt

    def update_healthFile(self, cf, private_key, name, surname):
        transaction = self.contract.functions.updatehealthFile(name,surname,cf).build_transaction({
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
        name, surname ,cfRecived = self.contract.functions.getHealthFile().call({'from': cf})
        healthFile = HealthFileData(name, surname, cfRecived)
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