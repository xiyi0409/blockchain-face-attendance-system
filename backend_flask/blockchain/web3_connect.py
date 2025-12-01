from web3 import Web3
import json
import os

class BlockchainConnector:
    def __init__(self):
        provider = "http://127.0.0.1:8545"  # Geth RPC
        self.web3 = Web3(Web3.HTTPProvider(provider))

        abi_path = os.path.join(os.path.dirname(__file__), "contract_abi.json")
        with open(abi_path, "r") as f:
            contract_abi = json.load(f)

        contract_address = os.getenv("CONTRACT_ADDRESS")
        self.contract = self.web3.eth.contract(
            address=contract_address,
            abi=contract_abi
        )

    def add_record(self, cid, employee_id):
        account = self.web3.eth.accounts[0]

        tx = self.contract.functions.addRecord(cid, employee_id).build_transaction({
            "from": account,
            "gasPrice": self.web3.to_wei("1", "gwei")
        })

        signed = self.web3.eth.account.sign_transaction(tx, "YOUR_PRIVATE_KEY")
        tx_hash = self.web3.eth.send_raw_transaction(signed.rawTransaction)
        return self.web3.to_hex(tx_hash)
