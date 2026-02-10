# file: c:\Users\etern\Downloads\frida-server-17.6.2-android-arm64\test.py
import base64
import hashlib
import json
import time
import random
import requests
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5

PUB_HEX = "30819f300d06092a864886f70d010101050003818d0030818902818100b8d1c40d42377d7b8601ad56965e4d5ec9f7112446eab0b9ba4f6fd717a6695de073dc9933490d63c32450d871823497135bfc1a016b8c8e1bb9b07653363b48f13cd960d4bb3ff66e4a4c2ff7d6b1e6c65322c15bf5db295688ff5ba790f62e4fe3ddcb122e48b787cba1fa1c6c13bae5a0008b4487990df3b9108c6e46ed910203010001"
PRI_HEX = "30820276020100300d06092a864886f70d0101010500048202603082025c02010002818100ceb1552c39e8aaeb03f8dba1c0a9936c37948ae52a17b29b20b69a0f88ab68021b8409775d3555294d6e8fa6362fde687cc70009e5876a39acc81bc30ee535bdb9148ad56bf5e1cf37d8c456ad14d68b8644bc5c7f40c8571ed3fbf4489f5346be3e39e1ecba93c93de0a882e44465e31303e2e125fb378b2f8a285dc9ca576502030100010281806893f2db40a5872d07c27725dd3c2f7a169912b9a6557d29de2065ccac42c58a236fe7f63bf3cb15edb69df9e3face5621a3f2520f8f3760dd1a1669d7f482fe84ef4bcd2c8453c25ad5dbcd8620cfece5f8cb533c57e7f116b3a0054e00ec78a7f033e7016bc51aa7da606c07ed87d7d105542bbea144effbb8e41196807995024100f74a202e60af8d66352653c8d42c0cdbc01e744d560aa8bc3ab0d8c47de6d0af10823a157a449a0adfa51afea6e5e9c49ae4589cd1abb3e730fee5943f26489b024100d5f922789885dbcc14e07aa4448f47018a94dbb024215c75048ab951543a040b1660a138ee6dbdd87c88ec9ee9327aff33e7a2a7af35d1012a9ce5560c4bdfff0240256a75cc0e9d014c01a6b6eea00bba3655af45f19d9f2740b3b0a65bb4a103da39293b189cd35c6b60c35e7e414a70406b1f39b92090563c18d1b872e1cb2d19024064860fc8c23718e4cee60b180351a0953bcae54ee21a7e3a4770f8d11995cbf27d87d6164e05668c3f2d80a4c37fc0c3065a8b52e6008d7953d0b3f971fb6f77024100cc770d2045c5f6af84022f2d40fbc3b27ee6659564d48224188a2181c07f43de07cb18dbd1d2fd2e79023f770c80091f36c202366213b491348a4c31595a1025"

SN = "B651CNW2FN2C006000000"
MODEL = "B651 NO_EEA_M2"
V_NAME = "HiBreak pro"

def encrypt_multi_block(plain_text, pub_hex):
    key = RSA.import_key(bytes.fromhex(pub_hex))
    cipher = PKCS1_v1_5.new(key)
    data = plain_text.encode('utf-8')
    res = b""
    chunk_size = 117
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        res += cipher.encrypt(chunk)
    return base64.b64encode(res).decode('utf-8')

def decrypt_multi_block(b64_data, pri_hex):
    try:
        key = RSA.import_key(bytes.fromhex(pri_hex))
        cipher = PKCS1_v1_5.new(key)
        ciphertext = base64.b64decode(b64_data)
        res = b""
        for i in range(0, len(ciphertext), 128):
            block = ciphertext[i:i+128]
            decrypted_block = cipher.decrypt(block, b"FAILED")
            res += decrypted_block
        return res.decode('utf-8', errors='ignore')
    except Exception as e:
        return f"Decryption error: {str(e)}"

def run_ota_capture():
    session = requests.Session()
    

    REAL_VERSION = "3.0.6"

    QUERY_VERSION = "3.0.6" 

    print(f"[*] Step 1: Performing device registration (Version: {REAL_VERSION})...")
    reg_data = {
        "deviceSn": SN,
        "productModel": MODEL,
        "versionCode": REAL_VERSION,
        "versionName": V_NAME
    }
    reg_headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 14; HiBreak Build/UP1A.231005.007)",
        "lang": "en_US"
    }
    reg_resp = session.post("http://ereader.bigme.vip:8081/xrzApp", json=reg_data, headers=reg_headers)
    print(f"    - Registration response: {reg_resp.text}")

    print(f"\n[*] Step 2: Checking firmware update (Probing version: {QUERY_VERSION})...")

    ts = time.strftime("%y%m%d%H%M%S")
    xrz_none = f"REQ-{ts}-{'%06x' % random.randint(0, 0xFFFFFF)}"
    
    query_json = {
        "osVersion": QUERY_VERSION,
        "xrz_none": xrz_none,
        "sn": SN,
        "osName": MODEL
    }


    sign_str = f"osName={MODEL};osVersion={QUERY_VERSION};sn={SN};xrz_none={xrz_none}"
    sign = hashlib.md5(sign_str.encode()).hexdigest()

    # Encrypt payload
    payload = json.dumps(query_json, separators=(',', ':'))
    encrypted_payload = encrypt_multi_block(payload, PUB_HEX)

    query_headers = {
        "xrz_sign": sign,
        "lang": "en",
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "okhttp/4.9.1",
        "Host": "usa.bigme.vip:8090"
    }

    resp = session.post("http://usa.bigme.vip:8090/json/osupgrade.action", data=encrypted_payload, headers=query_headers)
    
    if resp.status_code == 200:
        result = decrypt_multi_block(resp.text, PRI_HEX)
        print("\n--- Firmware query decryption result ---")
        print(result)
    else:
        print(f"Request failed: {resp.status_code}")

if __name__ == "__main__":
    run_ota_capture()