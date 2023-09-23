from pymongo.mongo_client import MongoClient
import pandas as pd
import json

# uniform resource indentifier
MONGODB_URI = "mongodb+srv://SufiyanisticGuy:sufi7000@cluster0.dcxialt.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(MONGODB_URI)

# create database name and collection name
DATABASE_NAME="pwskills_project"
COLLECTION_NAME="breast_cancer"

collection = client[DATABASE_NAME][COLLECTION_NAME]


retrieved_data = list(collection.find())
# Convert the data to a DataFrame
retrieved_dataframe = pd.DataFrame(retrieved_data)

# print(retrieved_dataframe.head())

if "_id" in retrieved_dataframe.columns.to_list():
     df = retrieved_dataframe.drop(columns=["_id"], axis=1)
 
     
# print(df.head())

