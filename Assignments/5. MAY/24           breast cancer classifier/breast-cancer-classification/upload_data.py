from pymongo.mongo_client import MongoClient
import pandas as pd
from sklearn.datasets import load_breast_cancer
import json

# uniform resource indentifier
MONGODB_URI = "mongodb+srv://SufiyanisticGuy:sufi7000@cluster0.dcxialt.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(MONGODB_URI)

# create database name and collection name
DATABASE_NAME="pwskills_project"
COLLECTION_NAME="breast_cancer"

#load the breast cancer dataset
breast_cancer_data = load_breast_cancer()

#convert the data into a pandas DataFrame
df = pd.DataFrame(data=breast_cancer_data.data, columns=breast_cancer_data.feature_names)

#add the target column to the DataFrame
df['target'] = breast_cancer_data.target


# Convert the data into json
json_record=list(json.loads(df.T.to_json()).values())

#now dump the data into the database
client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)