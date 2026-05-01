import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

print("🔥 Firebase DEBUG STARTED")

# 1) قراءة السيكرت
cred_json = os.getenv("FIREBASE_CREDENTIALS")

print("\n===== STEP 1: ENV CHECK =====")
print("ENV EXISTS:", cred_json is not None)

if not cred_json:
    raise Exception("❌ FIREBASE_CREDENTIALS is missing")

print("RAW LENGTH:", len(cred_json))
print("RAW FIRST 200 CHARS:\n", cred_json[:200])

# 2) محاولة parsing JSON
print("\n===== STEP 2: JSON PARSE =====")
try:
    cred_dict = json.loads(cred_json)
    print("✅ JSON parsed successfully")
except Exception as e:
    print("❌ JSON ERROR:", str(e))
    print("RAW CONTENT (safe preview):", repr(cred_json[:300]))
    raise

# 3) التحقق من أهم الحقول
print("\n===== STEP 3: VALIDATION =====")
required_keys = ["type", "project_id", "private_key", "client_email"]

for k in required_keys:
    print(f"{k}:", "OK" if k in cred_dict else "MISSING")

# 4) اختبار private_key
print("\n===== STEP 4: PRIVATE KEY CHECK =====")
pk = cred_dict.get("private_key", "")
print("private_key exists:", bool(pk))
print("private_key starts:", pk[:30])

if "\\n" not in pk:
    print("⚠️ WARNING: private_key missing newlines format")

# 5) Firebase init
print("\n===== STEP 5: FIREBASE INIT =====")
try:
    cred = credentials.Certificate(cred_dict)

    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    db = firestore.client()

    print("✅ FIREBASE INIT SUCCESS")
except Exception as e:
    print("❌ FIREBASE INIT FAILED:", str(e))
    raise

print("🔥 DEBUG FINISHED SUCCESSFULLY")
