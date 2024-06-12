from TrustAnchor import data, params
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
import json

isExit = False
isParamDefined = False

while not isExit:
    if not isParamDefined:
        print("1. Initialize System Parameters")
        print("2. Exit")
        choice = input("Choose: ")

        if choice == '1':
            print("Initialize System Parameters")
            params.init_parameters()
            isParamDefined = True
            print("System Parameters initialized!")
            print()
        elif choice == '2':
            isExit = True
        else:
            print("Invalid choice")
        continue
    print()
    print("Menu:")
    print("1. Register Smart Meter")
    print("2. Register Service Provider")
    print("3. Authenticate Smart Meter to Service Provider")
    print("4. Exit")
    choice = input("Choose: ")

    if choice == '1':
        print("Register Smart Meter")
        sm_id = input("Enter Smart Meter ID: ")
        priv, pub_sp = data.regist_SM(sm_id)
        print("Smart Meter registered")
    elif choice == '2':
        print("Register Service Provider")
        sp_id = input("Enter Service Provider ID: ")
        priv = data.regist_SP(sp_id)
        print("Service Provider registered")
    elif choice == '3':
        print("Authenticate Smart Meter to Service Provider")
        sm_id = input("Enter Smart Meter ID: ")
        sm = next((sm for sm in data.SM if sm.sm_id == sm_id), None)
        if not sm:
            print("Smart Meter not found")
            continue
        
        sp_id = sm.sp_id
        sp = next((sp for sp in data.SP if sp.sp_id == sp_id), None)
        if not sp:
            print("Service Provider not found")
            continue
        
        pub_sp = sp.public_key
        
        print("Smart Meter public key:")
        print(sm.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8'))
        
        print("Service Provider public key:")
        print(pub_sp.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8'))
        
        print("Authenticate Smart Meter to Service Provider")
        print("Smart Meter sign message")
        
        message = {
            'meter_id': sm_id,
            'timestamp': '2024-06-12T00:00:00',
            'power': 1000,
        }
        message_bytes = json.dumps(message).encode('utf-8')
        priv_sm = next((priv for sm_ in data.SM if sm_.sm_id == sm_id), None)
        
        if not priv_sm:
            print("Private key for the Smart Meter not found")
            continue
        
        signature = priv_sm.sign(message_bytes, ec.ECDSA(hashes.SHA256()))
        
        print("Smart Meter signature:")
        print(signature.hex())
        
        print("Service Provider verify signature")
        
        try:
            sm.public_key.verify(signature, message_bytes, ec.ECDSA(hashes.SHA256()))
            print("Authenticate success")
            print()
        except Exception as e:
            print("Invalid signature")
            print(f"Error: {e}")
            print()
    elif choice == '4':
        isExit = True
    else:
        print("Invalid choice")
