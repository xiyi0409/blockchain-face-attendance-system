import ipfshttpclient

def upload_to_ipfs(file_obj):
    """
    將上傳的圖片檔 (Werkzeug FileStorage) 直接傳到 IPFS，
    回傳 CID (字串)。
    """
    # 連線到本機 IPFS 節點 (Kubo)
    client = ipfshttpclient.connect("/ip4/127.0.0.1/tcp/5001")

    # 讀取檔案內容成 bytes
    data = file_obj.read()

    # 上傳 bytes，取得 CID
    cid = client.add_bytes(data)

    # 如果之後還要重複讀檔，可以 file_obj.seek(0)
    return cid
