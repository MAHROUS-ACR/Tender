import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

print("🔥 Firebase starting...")

firebase_json = os.getenv("FIREBASE_CREDENTIALS")

if not firebase_json:
    raise Exception("Missing Firebase secret")

try:
    cred_dict = json.loads(firebase_json)
except Exception as e:
    raise Exception(f"Invalid Firebase JSON: {e}")

cred = credentials.Certificate(cred_dict)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

print("✅ Firebase OK")
