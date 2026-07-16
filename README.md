# Digital Munshi AI - Milestone 1: Dataset Selection & Data Preprocessing

This repository contains the dataset, code, and documentation for the first implementation milestone of **Digital Munshi AI**, a legal technology assistant for Pakistan. This milestone covers dataset selection, understanding, and preprocessing to prepare a clean, machine learning-ready corpus.

## Project Structure
```
digital_munshi_ai/
├── pakistan_legal_cases_raw.csv   # The raw generated Pakistani legal case dataset
├── generate_dataset.py            # Python script used to simulate the raw data with noise
├── generate_report.py             # Python script to generate the PDF report
├── create_notebook.py             # Python script to create the Jupyter notebook
├── preprocessing.ipynb            # Jupyter notebook performing full EDA and preprocessing
├── data_preprocessing_report.pdf  # PDF report summarizing the dataset and preprocessing pipeline
└── README.md                      # Project documentation and setup guide
```

---

## Dataset Overview

The dataset represents user legal queries and case metadata across Pakistan's legal domain. It has a total of 1,215 records and 8 attributes:
- `case_id`: Unique identifier (e.g. `PK-LHR-2026-0001`).
- `date`: Date of query submission.
- `court_level`: Categorical attribute indicating the level of court (`District Court`, `High Court`, `Supreme Court`).
- `language`: Query language (`English`, `Urdu`).
- `client_type`: Type of legal client (`Individual`, `Corporate`, `NGO`, `Government`).
- `user_query`: Text field containing the raw user legal query.
- `severity_score`: Numerical value indicating urgency (1.0 to 10.0), with synthetic missing values and outliers.
- `primary_category` (Target): 6 target categories: `Criminal`, `Family`, `Property`, `Labor`, `Tenant`, and `Consumer`.

---

## Preprocessing Pipeline

The preprocessing steps implemented inside `preprocessing.ipynb` include:
1. **Deduplication:** Removal of duplicate records.
2. **Missing Value Treatment:** Mode imputation for `client_type` and Median imputation for `severity_score`.
3. **Outlier Treatment:** IQR-based clipping of `severity_score` outliers.
4. **Categorical Encoding:** One-Hot Encoding for categorical features (`court_level`, `language`, `client_type`).
5. **Text Vectorization:** Cleaning raw user queries and applying TF-IDF Vectorization.
6. **Feature Scaling:** Z-score Standardization of numerical attributes.
7. **Class Imbalance Resolution:** Applying **SMOTE-Tomek** to handle the severe class imbalance and obtain balanced target proportions.

---

## Installation and Execution

To run the preprocessing notebook and execute the scripts locally, follow these steps:

### 1. Clone/Setup the Project Directory
Make sure you are in the project folder:
```bash
cd digital_munshi_ai
```

### 2. Install Required Packages
Install the dependencies using pip:
```bash
pip install pandas numpy scikit-learn matplotlib seaborn imbalanced-learn reportlab
```

### 3. Run Preprocessing or Generate Reports
- To regenerate the raw dataset:
  ```bash
  python generate_dataset.py
  ```
- To regenerate the PDF report:
  ```bash
  python generate_report.py
  ```
- To open and run the notebook:
  ```bash
  jupyter notebook preprocessing.ipynb
  ```
