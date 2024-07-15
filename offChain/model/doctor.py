import json
from collections import namedtuple
from web3 import Web3

from offChain.model.model import Model

provider_url = "http://ganache:8080"
DoctorData = namedtuple('DoctorData', ['name', 'surname', 'cf'])
class Doctor(Model):
    def __init__(self, provider_url):
        super().__init__(provider_url,'doctor')

    def create_doctor(self, account, private_key, name, surname, cf):
        transaction = self.contract.functions.createDoctor(name, surname, cf).build_transaction({
            'from': account,
            'nonce': self.web3.eth.getTransactionCount(account),
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei')
        })

        signed_txn = self.web3.eth.account.signTransaction(transaction, private_key=private_key)
        tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        return receipt

    def update_doctor(self, cf, private_key, name, surname):
        transaction = self.contract.functions.updateDoctor(name, surname, cf).build_transaction({
            'from': cf,
            'nonce': self.web3.eth.getTransactionCount(cf),
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei')
        })

        signed_txn = self.web3.eth.account.signTransaction(transaction, private_key=private_key)
        tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        return receipt

    def get_doctor(self, cf):
        name, surname, cf1, password= self.contract.functions.getDoctor().call({'from': cf})
        doctor = DoctorData(name, surname, cf1,password)
        return doctor
"""
Esempio di utilizzo:
contract_address = "0xYourSmartContractAddress"
abi = json.loads('[{"inputs":[{"internalType":"string","name":"_nome","type":"string"},{"internalType":"string","name":"_cognome","type":"string"},{"internalType":"string","name":"_codiceFiscale","type":"string"}],"name":"creaDottore","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_nome","type":"string"},{"internalType":"string","name":"_cognome","type":"string"},{"internalType":"string","name":"_codiceFiscale","type":"string"}],"name":"aggiornaDottore","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getDottore","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]')

account = "0xYourEthereumAddress"
private_key = "YourPrivateKey"

dottore = Dottore(provider_url, contract_address, abi)
# Creazione di un nuovo dottore
receipt_crea = dottore.crea_dottore(account, private_key, "Mario", "Rossi", "ABCDEF12G34H567I")
print(receipt_crea)

# Aggiornamento di un dottore esistente
receipt_aggiorna = dottore.aggiorna_dottore(account, private_key, "Mario", "Bianchi", "ABCDEF12G34H567I")
print(receipt_aggiorna)

# Recupero dei dati del dottore
dottore_info = dottore.get_dottore(account)
print(dottore_info)"""
