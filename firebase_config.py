import os
import json
import base64
import firebase_admin
from firebase_admin import credentials, firestore

print("🔥 Firebase starting...")

cred_b64 = os.getenv("FIREBASE_CREDENTIALS_B64")

if not cred_b64:
    raise Exception("Missing Firebase secret")

cred_json = base64.b64decode(cred_b64).decode("utf-8")
cred_dict = json.loads(cred_json)

cred = credentials.Certificate(cred_dict)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

print("✅ Firebase OK")
