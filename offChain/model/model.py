import json

from web3 import Web3


class Model:

    def __init__(self, provider_url,contract_name):
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        try:
            abi= self.get_contract_abi(contract_name)
            address=self.get_contract_address(contract_name)
            self.contract = self.w3.eth.contract(address=address, abi=abi)
        except Exception as e:
            self.deploy_contract(contract_name)

    def get_contract_abi(self, contract_name):
        with open(f'onChain/abi/{contract_name}.txt') as f:
            contract_abi = json.load(f)
        return contract_abi

    def get_contract_address(self, contract_name):
        with open(f'onChain/address/{contract_name}.txt') as f:
            contract_address = f.read().strip()
        return contract_address

    def deploy_contract(self, contract_name):
        pass