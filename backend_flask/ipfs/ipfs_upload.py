import ipfshttpclient

def upload_to_ipfs(file_path):
    client = ipfshttpclient.connect("/ip4/127.0.0.1/tcp/5001")  
    result = client.add(file_path)
    return result["Hash"]
