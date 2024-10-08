import json
import os

from solcx import install_solc, get_installed_solc_versions, compile_standard
from web3 import Web3
import random
from eth_account import Account

class Model:
    def __init__(self, provider_url,contract_name, conn, solc_version='0.8.0'):
        self.solc_version = solc_version
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract= None
        self.deploy_contract(contract_name)
        self.conn=conn


    def deploy_contract(self, contract_name):
        try:
            contract_full_path = 'onChain/' + contract_name + '.sol'
            with open(contract_full_path, 'r') as f:
                contract_source_code = f.read()
            self.compile_contract(contract_source_code, contract_name)
        except Exception as e:
            print('Contratti inesistenti')

    def compile_contract(self, contract_source_code, contract_name):
        if self.solc_version not in get_installed_solc_versions():
            install_solc(self.solc_version)

        compiled_sol = compile_standard({
            "language": "Solidity",
            "sources": {f"onChain/{contract_name}.sol": {"content": contract_source_code}},
            "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}}
        }, solc_version=self.solc_version)

        self.contract_id, self.contract_interface = next(iter(compiled_sol['contracts'][f"onChain/{contract_name}.sol"].items()))
        self.abi = self.contract_interface['abi']
        self.bytecode = self.contract_interface['evm']['bytecode']['object']
        account = self.loadAdmin()
        contract = self.web3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        tx_hash = contract.constructor().transact({'from': account})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        self.contract = self.web3.eth.contract(address=tx_receipt.contractAddress, abi=self.abi)
        with open(f'onChain/address/{contract_name}.txt', 'w') as file:
            file.write(self.contract.address)
        with open(f'onChain/abi/{contract_name}.json', 'w') as file:
            json.dump(self.contract.abi, file)

    def cf_to_address(self, cf):
        cursor = self.conn.cursor(dictionary=True)

        # Esecuzione della query con un filtro per CF
        query = "SELECT * FROM users WHERE cf = %s"
        cursor.execute(query, (cf,))

        # Recupero di una singola riga
        result = cursor.fetchone()
        return result

    def create_new_account(self):

        new_account = Account.create()
        address = new_account.address
        private_key = new_account._private_key.hex()

        return address, private_key

    def loadAdmin(self):
        with open("offChain/credential/credential.json", 'r') as file:
            data = json.load(file)
        return data["address"]