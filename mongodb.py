from pymongo import MongoClient
import datetime
client = MongoClient('mongodb://localhost:27017/')
print(client.list_database_names())
db = client.RagVignerons  # db = client['RagVignerons']
collection = db.page_pdf  # db = db['page_pdf']

post = {
    "author": "Mike",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.now(tz=datetime.timezone.utc),
}
collection.insert_one(post).inserted_id
