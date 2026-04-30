import firebase_admin
from firebase_admin import credentials, firestore

# قراءة ملف الخدمة اللي بيتعمل من GitHub Actions
cred = credentials.Certificate("serviceAccount.json")

# منع إعادة التهيئة لو الملف اتنفذ أكتر من مرة
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()
