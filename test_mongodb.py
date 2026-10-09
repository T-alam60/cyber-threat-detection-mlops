from pymongo import MongoClient
uri = "mongodb+srv://tanjir233159_db_user:YOUR_PASSWORD@cluster0.v7mhlis.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)
try:
    client.admin.command("ping")
    print("Connected successfully")
    client.close()

except Exception as e:
    raise Exception(
        "The following error occurred: ", e)