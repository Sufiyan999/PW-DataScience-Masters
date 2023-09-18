
# Breast Cancer Type Classification with Machine Learning

This project is an end-to-end machine learning application built with Flask and Python to classify breast cancer types using the scikit-learn library. It provides a simple web interface to train machine learning models and make predictions on new data.


---

## Models Used

- XGBoost Classifier
- Support Vector Classifier (SVC)
- Random Forest Classifier

## Dataset

The dataset used for this project is the Breast Cancer dataset from scikit-learn's `load_breast_cancer` module.

## Getting Started

1. Clone this repository to your local machine.

```bash
git clone https://github.com/Sufiyan999/breast-cancer-classification
```
2. Environment setup:

```bash
 conda create --prefix venv python==3.8 -y
 conda activate venv/
```

3. Install the required dependencies.

```bash
pip install -r requirements.txt
```

4. Start the Flask application.

```bash
python app.py
```

5. Access the application in your web browser at `http://localhost:5000`.

## Usage

### Training the Models

1. Visit `/train` on the web application to train the machine learning models. The application will download the dataset from your MongoDB database and train each model.

### Making Predictions

1. Visit `/predict` on the web application.
2. Upload a CSV file containing breast cancer data for prediction.
3. Click the "Predict" button to classify the cancer type.

## MongoDB Integration

This project integrates with MongoDB for dataset storage. Make sure to provide your MongoDB credentials in the configuration.

```python
# upload_data.py

MONGODB_URI = "mongodb+srv://<username>:<password>@cluster0.dcxialt.mongodb.net/?retryWrites=true&w=majority"#your_mongodb_uri_here
```

## **Built With**
- Flask
- Python
- Machine Learning
- Scikit-learn


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- The scikit-learn and Flask communities for their excellent libraries and resources.
- [Data Source: Breast Cancer Wisconsin (Diagnostic) Data Set](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic))

## Contact

If you have any questions or suggestions, please feel free to contact the project maintainers:

- Moh Sufiyan - [mail](sufiyanmoh999@gmail.com)

---




<!-- This is a simple flask app for classifying breast cancer type. This project was given to us as an assignment. -->

<!-- 
**Dataset is taken from sklearn.load_datasets**

# Installing
1. Environment setup:
> conda create --prefix venv python==3.8 -y
> conda activate venv/

2. Install required packages:
> pip install -r requirements.txt

3. Run application:
> python app.py -->

