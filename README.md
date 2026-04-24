# Interest Compatibility App

## Overview
This project is a Python-based application that analyzes compatibility between users based on their content interests. It processes user activity data, extracts themes from content titles, and computes similarity scores using TF-IDF and cosine similarity.

The application includes an interactive Streamlit interface.

---

## Features
- Overall compatibility analysis between multiple users
- Direct comparison between two users
- Single user interest analysis
- Visualization using charts and heatmaps

---

## Methodology

### Data Processing
User data is loaded from CSV files containing content titles.

### Theme Classification
Titles are classified into themes using:
- Keyword matching
- Hashtag detection

### Feature Representation
Theme counts are converted into numerical vectors.

### TF-IDF Weighting
Themes are weighted using:
- Term Frequency (TF)
- Inverse Document Frequency (IDF)

### Similarity Calculation
Cosine similarity is used to compute compatibility scores.

---

## Project Structure

```
streamlit_app.py       # Main Streamlit interface
similarity.py          # TF-IDF and similarity logic
classifier.py          # Theme classification
data_loader.py         # Data loading
visualize.py           # Visualization functions
main.py                # Testing script
README.md              # Project documentation
```

---

## How to Run

### Install dependencies
```
pip install pandas streamlit matplotlib
```

### Run the application
```
streamlit run streamlit_app.py
```

---

## Input Format

CSV files must contain:

```
user,title,date,source
```

Example:
```
Alice,Python tutorial,2024-01-01,youtube
```

---

## Limitations
- The classification system is keyword-based and may produce incorrect matches
- The model does not understand semantic meaning
- Results depend on input data quality
- TF-IDF may not be effective for very small datasets

---

## Future Improvements
- Use NLP models for better classification
- Improve theme grouping
- Enhance UI design

---

## Author
Gayden Jamba

---

## GitHub Repository
(https://github.com/gjambaieu2025-netizen/Interest-Compatibility-App)
