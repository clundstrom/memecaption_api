import firebase_admin
from firebase_admin import credentials, firestore


def updateStatus():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    fb = firestore.client()
    ref = fb.collection(u'api').document(u'j087hhlFv3IHzcz89OAZ')
    ref.update({
        u'api_online': 1,
        u'last_online': firestore.SERVER_TIMESTAMP
    })