import firebase_admin
from firebase_admin import credentials, firestore

# auth
cred = credentials.Certificate("/home/prashanth/Desktop/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()  # this connects to our Firestore database
collection = db.collection('groups')  # opens 'groups' collection
doc = collection.document('new_doc_id')  # specifies the 'new_doc_id' document

# Get

_doc = collection.document('new_doc_id')
res = _doc.get().to_dict()
print(res)

# We can also perform a .get() operation on collection to return an array of all documents contained within it. If we had two documents, it would look like this

docs = collection.get()
# print(docs[0].to_dict())

# Create

res = collection.document('barcelona').set({
    'lat': 41.3851, 'long': 2.1734,
    'weather': 'great',
    'landmarks': [
        'guadí park',
        'gaudí church',
        'gaudí everything'
    ]
})

print(res)

docs = collection.get()
print([docs[i].to_dict() for i in docs])

# Modify

# To update a full key-value pair, we use update

res = collection.document('barcelona').update({
    'weather': 'sun'
})

# TO update in Arrays

collection.document('barcelona').update({
    'landmarks': firestore.ArrayUnion(['colosseum'])
})

# And to remove vatican_city and trastevere
collection.document('rome').update({
    'where_to_go': firestore.ArrayRemove(
        ['vatican_city', 'trastevere']
    )})

# Delete
res = collection.document('test_1').set({
    'lat': 41.3851, 'long': 2.1734,
    'weather': 'summer',
    'landmarks_2': [
        'guadí park',
        'gaudí church',
        'gaudí everything'
    ]
})

collection.document('test_1').delete()

# If we wanted to delete a single field within a document, we could use firestore.DELETE_FIELD like so

collection.document('barcelona').update({
    'weather': firestore.DELETE_FIELD})

# Query

# syntax = where(fieldPath, opStr, value)

'''
fieldPath — the field we are targeting, in this case 'long'
opStr — comparison operation string, '==' checks equality
value — the value we are comparing to
'''

collection.where('long', '>', 9.4989).get()
