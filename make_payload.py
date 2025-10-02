import pickle, base64, sys
payload = pickle.dumps({"role": "admin", "exp": 999999999})
sys.stdout.write(base64.b64encode(payload).decode())
