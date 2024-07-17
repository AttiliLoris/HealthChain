import json
from solcx import install_solc, get_installed_solc_versions, compile_standard
from web3 import Web3
import random

class Model:

    def __init__(self, provider_url,contract_name, solc_version='0.8.0'):
        self.solc_version = solc_version
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        try:
            abi= self.get_contract_abi(contract_name)
            address=self.get_contract_address(contract_name)
            self.contract = self.web3.eth.contract(address = address, abi = abi)
        except Exception as e:
            self.deploy_contract(contract_name)

    def get_contract_abi(self, contract_name):
        with open(f'onChain/abi/{contract_name}.json') as f:
            contract_abi = json.load(f)
        return contract_abi

    def get_contract_address(self, contract_name):
        with open(f'onChain/address/{contract_name}.txt') as f:
            contract_address = f.read().strip()
        return contract_address

    def deploy_contract(self, contract_name):
        with open(f'onChain/{contract_name}.sol') as f:
            contract_source_code = f.read()
        self.compile_contract(contract_source_code, contract_name)

    def compile_contract(self, contract_source_code, contract_name):
        if self.solc_version not in get_installed_solc_versions():
            install_solc(self.solc_version)

        # Compile the Solidity source code
        compiled_sol = compile_standard({
            "language": "Solidity",
            "sources": {f"on_chain/{contract_name}.sol": {"content": contract_source_code}},
            "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}}
        }, solc_version=self.solc_version)

        # Extract the ABI and bytecode
        self.contract_id, self.contract_interface = next(iter(compiled_sol['contracts'][f"on_chain/{contract_name}.sol"].items()))
        self.abi = self.contract_interface['abi']
        self.bytecode = self.contract_interface['evm']['bytecode']['object']
        account = random.choice(self.web3.eth.accounts)
        # Create the contract in Web3
        contract = self.web3.eth.contract(abi=self.abi, bytecode=self.bytecode)

        # Send transaction to deploy the contract
        tx_hash = contract.constructor().transact({'from': account})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        self.contract = self.web3.eth.contract(address=tx_receipt.contractAddress, abi=self.abi)

        with open(f'on_chain/address/{contract_name}.txt', 'w') as file:
            file.write(self.contract.address)
        with open(f'on_chain/abi/{contract_name}.json', 'w') as file:
            json.dump(self.contract.abi, file)