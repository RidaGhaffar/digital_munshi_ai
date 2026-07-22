# Digital Munshi AI - Legal Tech Assistant for Pakistan

This repository contains the dataset, code, and documentation for the implementation milestones of **Digital Munshi AI**, a legal technology assistant for Pakistan.

## Project Structure
```
digital_munshi_ai/
├── pakistan_legal_cases_raw.csv   # The raw generated Pakistani legal case dataset
├── generate_dataset.py            # Python script used to simulate the raw data with noise
├── generate_report.py             # Python script to generate the PDF report
├── create_notebook.py             # Python script to create the preprocessing notebook (Milestone 1)
├── preprocessing.ipynb            # Unified Jupyter notebook for Preprocessing, Feature Engineering & EDA (Milestones 1 & 2)
├── data_preprocessing_report.pdf  # PDF report summarizing the dataset and preprocessing pipeline
├── verify_eda.py                  # Verification script for feature engineering and pipeline execution
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

## Preprocessing Pipeline (Milestone 1)

The preprocessing steps implemented inside `preprocessing.ipynb` include:
1. **Deduplication:** Removal of duplicate records.
2. **Missing Value Treatment:** Mode imputation for `client_type` and Median imputation for `severity_score`.
3. **Outlier Treatment:** IQR-based clipping of `severity_score` outliers.
4. **Categorical Encoding:** One-Hot Encoding for categorical features (`court_level`, `language`, `client_type`).
5. **Text Vectorization:** Cleaning raw user queries and applying TF-IDF Vectorization.
6. **Feature Scaling:** Z-score Standardization of numerical attributes.
7. **Class Imbalance Resolution:** Applying **SMOTE-Tomek** to handle the severe class imbalance and obtain balanced target proportions.

---

## Feature Engineering & EDA (Milestone 2)

The feature transformations and exploratory visual insights implemented inside `preprocessing.ipynb` include:

### 1. Feature Engineering
* **Text Metadata Extraction:** Generated numeric attributes `query_length` and `word_count` to capture complexity differences in legal queries.
* **Temporal Feature Extraction:** Extracted `year`, `month`, and `month_name` from the case datetime. These are used to plot and investigate seasonal distributions of Pakistani legal cases.
* **Feature Selection (SelectKBest):** Applied **Mutual Information (MI)** ranking (`mutual_info_classif`) to isolate the top **25 most informative features** from the combined high-dimensional TF-IDF tokens and tabular features, removing irrelevant parameters like raw query strings and case IDs.

### 2. Exploratory Visualizations & Interpretations
* **Target Category Distribution:** Bar plots highlighting the initial severe class imbalance (Majority: Criminal & Property, Minority: Consumer & Labor).
* **Numerical Distributions:** KDE & Histograms of character lengths and word counts showing multi-modal user query distributions.
* **Outlier Boxplot:** Boxplots visualizing the extreme positive and negative outlier distribution in the raw `severity_score` column.
* **Categorical Counts:** Multi-class group counts for `court_level` (showing most queries are at District Court level) and `language` (verifying balance between English and Urdu).
* **Correlation Heatmap:** Visualized correlation scores to detect redundancy (confirming `query_length` and `word_count` have a 0.99 correlation, making one redundant).
* **Mutual Information Ranking Bar Chart:** Highlights the top-rated text tokens (e.g. `police`, `landlord`, `divorce`, `refrigerator`) as highly predictive features for specific legal classes.

---

## Installation and Execution

To run the notebooks and execute the scripts locally, follow these steps:

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

### 3. Run Notebooks
- To open and run the unified Preprocessing, Feature Engineering & EDA notebook:
  ```bash
  jupyter notebook preprocessing.ipynb
  ```
- To run the pipeline verification programmatically:
  ```bash
  python verify_eda.py
  ```


