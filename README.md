# AI-Based Phishing Email Detection System

Deployed link : https://phishing-email-detection-6m6b.onrender.com/

## Project Overview

The AI-Based Phishing Email Detection System is a machine learning-based web application designed to identify potentially phishing emails.

The system analyses email content and predicts whether an email is potentially phishing or legitimate. It uses Natural Language Processing (NLP) techniques and a Logistic Regression algorithm to classify email text based on patterns learned from a labelled dataset.

## Features

- Detects potentially phishing and legitimate emails.
- Uses a trained machine learning model for classification.
- Analyses email content using TF-IDF vectorization.
- Displays prediction results through a web interface.
- Shows the estimated phishing probability.
- Provides a responsive and user-friendly interface.

## Technologies Used

- **Programming Language:** Python
- **Frontend:** HTML, CSS, JavaScript
- **Machine Learning:** Scikit-learn
- **NLP Technique:** TF-IDF Vectorization
- **Classification Algorithm:** Logistic Regression
- **Data Processing:** Pandas
- **Model Storage:** Joblib
- **Web Server:** Gunicorn
- **Deployment Platform:** Render

## How It Works

1. A labelled email dataset is used to train the machine learning model.
2. TF-IDF converts email text into numerical features.
3. Logistic Regression learns patterns from the training data.
4. The trained model is saved as `phishing_model.pkl`.
5. Users enter email content through the website.
6. The model analyses the entered text and predicts its category.
7. The website displays the prediction and estimated phishing probability.

## Project Structure

```text
Phishing-Email-Detection/
│
├── main.py
├── server.py
├── wsgi.py
├── phishing_model.pkl
├── model_results.txt
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/AnkitaaBorade/Phishing-Email-Detection.git
```

### 2. Open the Project Folder

```bash
cd Phishing-Email-Detection
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application Locally

```bash
gunicorn wsgi:application
```

The application can then be accessed through the local server address displayed in the terminal.

## Machine Learning Model

The project uses Logistic Regression with TF-IDF vectorization.

The model is trained on labelled email data and learns text patterns associated with phishing and legitimate emails. The saved model is then used to classify new email content.

## Limitations

- The system analyses email text only.
- It does not independently verify sender identity or email headers.
- It does not inspect attachments or visit links.
- Predictions depend on the quality of the training dataset.
- The model may produce incorrect predictions.

## Disclaimer

This project is developed for educational and academic purposes. Its predictions are intended to assist in identifying suspicious emails and should not be treated as a guarantee of email safety.
