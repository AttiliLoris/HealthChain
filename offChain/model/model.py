from web3 import Web3


class Model:

    def __init__(self, provider_url,contract_name):
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract_name = contract_name
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=abi)
