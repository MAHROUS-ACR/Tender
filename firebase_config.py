import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

print("🔥 Firebase init starting...")

cred_json = os.getenv("FIREBASE_CREDENTIALS")

if not cred_json:
    raise Exception("❌ FIREBASE_CREDENTIALS is missing or empty")

try:
    cred_dict = json.loads(cred_json)
except Exception as e:
    raise Exception(f"❌ Invalid JSON in FIREBASE_CREDENTIALS: {e}")

cred = credentials.Certificate("path/to/FIREBASE_CREDENTIALS.json")
firebase_admin.initialize_app(cred)


if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

print("✅ Firebase ready")
