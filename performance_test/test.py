import time
import json  # Import json for serialization
import numpy as np
import matplotlib.pyplot as plt
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes


def test_curve(curve, num):
    # generate key pair
    private_key = ec.generate_private_key(curve)
    public_key = private_key.public_key()
    # data smart meter
    message = {
        'meter_id': '123456',
        'timestamp': '2020-01-01T00:00:00',
        'power': 1000,
    }
    # Serialize the dictionary to a JSON string and then to bytes
    message_bytes = json.dumps(message).encode('utf-8')
    
    # test signing
    start = time.time()
    for i in range(num):
        signature = private_key.sign(message_bytes, ec.ECDSA(hashes.SHA256()))
    end = time.time()
    sign_time = (end - start) / num
    
    # test verification
    start = time.time()
    for i in range(num):
        public_key.verify(signature, message_bytes, ec.ECDSA(hashes.SHA256()))
    end = time.time()
    verify_time = (end - start) / num
    return sign_time, verify_time


def main():
    curves = [ec.BrainpoolP256R1(), ec.BrainpoolP384R1(), ec.BrainpoolP512R1()]
    num = 100
    sign_time = []
    verify_time = []
    for curve in curves:
        s, v = test_curve(curve, num)
        sign_time.append(s)
        verify_time.append(v)
    x = np.arange(len(curves))
    plt.bar(x, sign_time, width=0.4, label='sign')
    plt.bar(x + 0.4, verify_time, width=0.4, label='verify')
    plt.xticks(x + 0.2, ['BrainpoolP256R1', 'BrainpoolP384R1', 'BrainpoolP512R1'])
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
