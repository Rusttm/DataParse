# from https://www.w3schools.com/python/python_mongodb_query.asp

from pymongo import MongoClient

# Подключение к серверу MongoDB
client = MongoClient('mongodb://root:example@localhost:27017/')

# Выбор базы данных и коллекции
db = client['books']
collection = db['books_collection']

# Запросs на выдачу из коллекции
# myquery = {"book_price": 16.64}   #equal
# myquery = {"book_price": { "$gt": 59 }}    #greater than
myquery = {"book_title": { "$regex": "[Mm]urder | [Dd]eath" }}
# myquery = {"book_description": { "$in": ["Murder", "Death"] }}    #for arrays include
query_result = collection.find(myquery)

print(f"Selected {len(list(query_result))} notes")

# Запрос с выводом только необходимой информации (проекции)
projection = {"_id": 0, "book_title": 1}
query_result_1 = collection.find(myquery, projection)

for x in query_result_1:
    print(x)

# UPDATE with new field - set
new_field_value = ["bestseller", "top10"]
collection.update_one({"book_title": "A Murder in Time"}, {"$set": {"notes": new_field_value}})
new_query = {"book_title": "A Murder in Time"}
new_projection = {"_id": 0, "book_title": 1, "notes": 1}
print(collection.find_one(new_query, new_projection))