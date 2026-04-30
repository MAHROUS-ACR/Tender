import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

cred_json = os.getenv("FIREBASE_KEY")  # 👈 نفس اسم السيكرت عندك

if not cred_json:
    raise Exception("FIREBASE_KEY is missing from environment variables")

cred_dict = json.loads(cred_json)

cred = credentials.Certificate(cred_dict)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
