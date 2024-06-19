from flask import Flask, jsonify
import jwt
import json
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

PRIVATE_KEY = os.getenv('PRIVATE_KEY')

@app.route('/.well-known/jwks.json')
def jwks():
    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(PRIVATE_KEY)
    jwk = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(public_key))
    jwks = {
        'keys': [jwk]
    }
    return jsonify(jwks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
