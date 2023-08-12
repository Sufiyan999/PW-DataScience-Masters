
# Local Project Setup

So, to set this project in local we have couple of steps needed. 

1. Environment creation
2. Mongodb Account setting
3. Environment variable settings
4. Aws configure 





## Environment creation

In this part, we will see how to create a conda environment. 

## Create a new Conda environment

Go to your project folder and open vscode/terminal there. To create a new Conda environment for this particular project, use the following command:

```bash
conda create --prefix ./env python=3.8
```

To activate the environment 
```bash
conda activate ./env 
```
if the environment activation code gives error, try this one 
```bash
source activate ./env
```
## MongoDb account setting

MongoDB is a popular NoSQL database that allows you to store and retrieve data in a flexible and scalable way. In this guide, we will go through the steps of creating a MongoDB account, database, and how to get the Python 3.8 client URL for MongoDB.

### Step 1: Create a MongoDB account

**To create a MongoDB account, follow these steps:**

1. Go to the MongoDB website and click on the "Sign Up" button.

2. Fill in the required details such as your name, email address, and password.

3. Verify your email address by clicking on the link sent to your email.

4. Once you have verified your email address, log in to your MongoDB account.

## Step 2: Create a MongoDB database

**To create a MongoDB database, follow these steps:**

1. Click on the "Create a Cluster" button on the MongoDB Atlas dashboard.

2. Choose the free plan by selecting the "Shared" option.

3. Choose your preferred cloud provider, region, and cluster name.

4. Click on the "Create Cluster" button.

5. Once the cluster is created, click on the "Collections" button to create a new collection in the database.

## Step 3: Get the Python 3.8 client URL

To get the Python 3.8 client URL for MongoDB, follow these steps:

1. Click on the "Connect" button on the MongoDB Atlas dashboard.

2. Select "Connect your Application".

3. Choose your preferred programming language ( for us python), version ( for us 3.6 or above), and driver.

4. Copy the Python 3.8 client URL provided.

5. Use the client URL to connect to your MongoDB database in Python.

## Step 4: Create s3 Bucket in AWS s3

1. Navigate to the S3 service in aws.
2. Click on the "Create bucket" button on the S3 dashboard.
3. In the "Create bucket" dialog, provide a unique name for your bucket. For our project, keep it `sensor-deployment` as we have mentioned this particular name for our project in our constant module. If you wanna give another name make sure you mention it inside the constant module.
4. Click on the "Create bucket" button to create your S3 bucket.


## Environment variable setting

**To set environment variables in Windows for AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and MONGO_DB_URL, you can follow these steps:**

- Open the Start menu and search for **Environment Variables**

- Click on **Edit the system environment variables**

Click on the **Environment Variables** button.

Under the **User variables** or **System variables** section, click **New**.

In the **Variable name** field, enter the name of the environment variable you want to set (e.g., AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, MONGO_DB_URL).

In the "Variable value" field, enter the corresponding value for the environment variable.

Click "OK" to save the environment variable.

**Note:**
- You will get *How to get the aws credentials* in the deployment documentation. 

**To set the environment variables in linux, use the following method to add any environment variable.

**AWS secret access key**
```bash
export AWS_ACCESS_KEY_ID=<your-access-key-id>
```

**AWS other credentials**
```bash
export AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
```

**MongoDB URL**
```bash
export MONGO_DB_URL=<your-mongodb-client-url>
```
## Aws configure 

- [Install Aws Cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) Depending on your **Os**.

**Configure AWS cli**

Run the following command in your pc terminal
```bash
aws configure
```
This will prompt you the aws credentials. 

    # Enter your AWS Access Key ID and Secret Access Key
    # Enter your Default region name (set it as ap-south-1 or wherever your s3, ec2 and ecr are present)
    # Enter your Default output format (e.g. json)

## Final Project Run

Once you have successfully completed the steps above, 
- Install the **requirements.txt** by running the following command 

To activate the environment
```bash
source activate ./env 
```
To install the dependencies
```bash
pip install -r requirements.txt
```

Once you are done with the libraries installation, 
Run
```bash
python app.py
```

Open your browser and hit the url belor

- [https://localhost:5000](https://localhost:5000)

The project should run now in your local pc. 
