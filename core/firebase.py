import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

cred = credentials.Certificate('PATH-TO-CREDENTIALS')
firebase_admin.initialize_app(
    cred, {'databaseURL': 'https://YOUR-DATABASE.firebaseio.com/'})

ref = db.reference('users')

def push_to_fb(user_id,obj=object):
    global ref
    ref_id = ref.child(user_id)
    ref_id.update(obj)
    

def create_to_fb(user_id):
    ref.update({
        user_id : {
            "numDeleted" : 0,
            "deleteAll" : False,
        }
    })

def get_from_fb(user_id):
    global ref
    ref_id = ref.child(user_id)
    result = ref_id.get()
    if (result == None):
        print('None')
        create_to_fb(user_id)
        return ref.child(user_id).get()
    return result


