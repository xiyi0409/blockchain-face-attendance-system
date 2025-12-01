from web3 import Web3
import json
import os

# 預設使用本機 Geth RPC
WEB3_PROVIDER_URI = os.getenv("WEB3_PROVIDER_URI", "http://127.0.0.1:8545")

# 智能合約地址、私鑰建議放在環境變數或 .env
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "0x0000000000000000000000000000000000000000")
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")

ABI_PATH = os.path.join(os.path.dirname(__file__), "contract_abi.json")


def _get_web3():
    return Web3(Web3.HTTPProvider(WEB3_PROVIDER_URI))


def _get_contract(w3: Web3):
    if not os.path.exists(ABI_PATH):
        raise FileNotFoundError(f"contract_abi.json not found at {ABI_PATH}")

    with open(ABI_PATH, "r", encoding="utf-8") as f:
        abi = json.load(f)

    if not CONTRACT_ADDRESS or CONTRACT_ADDRESS == "0x0000000000000000000000000000000000000000":
        raise ValueError("CONTRACT_ADDRESS 未設定，請在環境變數或 .env 中設定")

    address = w3.to_checksum_address(CONTRACT_ADDRESS)
    return w3.eth.contract(address=address, abi=abi)


def send_to_blockchain(cid: str, employee_id: str) -> str:
    """
    呼叫智能合約 addRecord(cid, employeeId)
    回傳交易哈希 TxHash（字串）
    """
    if not PRIVATE_KEY:
        raise ValueError("PRIVATE_KEY 未設定，請在環境變數或 .env 中設定")

    w3 = _get_web3()
    contract = _get_contract(w3)

    # 從私鑰取得發送帳號
    account = w3.eth.account.from_key(PRIVATE_KEY).address

    # 取得 nonce
    nonce = w3.eth.get_transaction_count(account)

    # 建立交易（使用 legacy gas，因為你是 Geth 私鏈）
    tx = contract.functions.addRecord(cid, employee_id).build_transaction({
        "from": account,
        "nonce": nonce,
        "gas": 300000,
        "gasPrice": w3.to_wei("1", "gwei")
    })

    # 簽署與送出交易
    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)

    return w3.to_hex(tx_hash)
