\# SupplyPrescript: AI-Powered Supply Chain Risk Prediction



\## Project Overview



SupplyPrescript is a machine learning-based supply chain risk prediction system designed to identify the risk classification of supply chain operations using logistics, supplier, inventory, and transportation data.



The project uses an XGBoost Classifier to predict supply chain risk levels and assists businesses in making informed decisions.



\---



\## Team



\- \*\*Team Leader:\*\* Syed Mohammed Khalid Hussaini

\- \*\*Project:\*\* SupplyPrescript

\- \*\*Domain:\*\* Data Analytics \& Machine Learning



\---



\## Project Workflow



```

Raw Dataset

&#x20;     │

&#x20;     ▼

Data Preprocessing

&#x20;     │

&#x20;     ▼

Feature Engineering

&#x20;     │

&#x20;     ▼

Data Preparation

&#x20;     │

&#x20;     ▼

Model Training

&#x20;     │

&#x20;     ▼

Model Evaluation

```



\---



\## Dataset



\- Total Records: \*\*113,097\*\*

\- Original Features: \*\*18\*\*

\- Features After Cleaning: \*\*16\*\*

\- Features After Engineering: \*\*20\*\*



Target Variable:



\- `risk\_classification`



\---



\## Completed Modules



\### 1. Data Preprocessing (`processing.py`)



Completed tasks:



\- Loaded raw dataset

\- Removed unnecessary columns

&#x20; - `product\_id`

&#x20; - `supplier\_id`

\- Checked missing values

\- Encoded target variable (`risk\_classification`)

\- Saved cleaned dataset



Output:



```

data/processed/cleaned\_supply\_chain.csv

```



\---



\### 2. Feature Engineering (`feature\_engineering.py`)



Created four business-oriented features:



| Feature | Description |

|---------|-------------|

| inventory\_coverage | Inventory available relative to historical demand |

| supplier\_efficiency | Supplier reliability adjusted by lead time |

| logistics\_risk | Shipping cost combined with route risk |

| delay\_impact | Expected impact of delivery delays |



Additional validation:



\- Duplicate check

\- Missing value check

\- Summary statistics



Output:



```

data/processed/feature\_engineered\_supply\_chain.csv

```



\---



\### 3. Data Preparation (`data\_preparation.py`)



Completed tasks:



\- Loaded feature engineered dataset

\- One-Hot Encoded `supplier\_country`

\- Separated features and target

\- Split dataset into training and testing sets

\- Used stratified sampling (80:20)



Generated files:



```

X\_train.csv

X\_test.csv

y\_train.csv

y\_test.csv

```



\---



\### 4. Model Training (`model\_training.py`)



Algorithm Used:



\- XGBoost Classifier



Training Parameters:



\- n\_estimators = 100

\- max\_depth = 6

\- learning\_rate = 0.1

\- random\_state = 42



Saved trained model:



```

models/xgboost\_model.pkl

```



\---



\### 5. Model Evaluation (`model\_evaluation.py`)



Evaluation Metrics:



\- Accuracy

\- Precision

\- Recall

\- F1 Score

\- Classification Report

\- Confusion Matrix

\- Feature Importance Analysis



\---



\## Model Performance



| Metric | Score |

|---------|-------|

| Accuracy | \*\*99.99%\*\* |

| Precision | \*\*99.99%\*\* |

| Recall | \*\*99.99%\*\* |

| F1 Score | \*\*99.99%\*\* |



\---



\## Feature Importance



The trained XGBoost model identified the following as the most influential features:



\- disruption\_likelihood\_score

\- supplier\_country

\- weather\_condition\_severity

\- inventory\_coverage

\- supplier\_reliability\_score



\---



\## Validation



To understand the exceptionally high model accuracy, a validation experiment was performed.



The most influential feature:



```

disruption\_likelihood\_score

```



was temporarily removed from the dataset.



Result:



| Model | Accuracy |

|---------|----------|

| Original Model | \*\*99.99%\*\* |

| Without `disruption\_likelihood\_score` | \*\*\~75.15%\*\* |



This confirms that `disruption\_likelihood\_score` is the strongest predictor in the dataset and contributes significantly to the model's performance.



\---
\# SupplyPrescript



\## Data Analytics Internship Project



SupplyPrescript is a supply chain analytics project developed as part of the Data Analytics Internship.



The objective of this project is to predict shipment delays using machine learning and provide data-driven recommendations to improve supply chain decisions.



\## Features



\- Shipment delay prediction

\- Data preprocessing and analysis

\- Machine learning model

\- Optimization-based recommendations

\- Backend API

\- Interactive dashboard



\## Project Structure



```

SupplyPrescript/

│

├── data/

│   ├── processed/

│   └── dynamic\_supply\_chain\_logistics\_dataset\_with\_country.csv

│

├── models/

│   └── xgboost\_model.pkl

│

├── notebooks/

│   ├── ML\_Workflow\_Demonstration.ipynb

│   └── Model\_Accuracy\_Analysis.ipynb

│

├── src/

│   ├── processing.py

│   ├── feature\_engineering.py

│   ├── data\_preparation.py

│   ├── model\_training.py

│   └── model\_evaluation.py

│

├── reports/

│

├── README.md

│

└── requirements.txt

```



\---



\## Technologies Used
├── src/

├── models/

├── optimization/

├── backend/

├── frontend/

├── notebooks/

├── reports/

├── docs/

└── README.md

```



\## Documentation



For team workflow, branch rules, responsibilities, and development guidelines, see:



\- `docs/TEAM\_GUIDE.md`



\## Technology Stack



\- Python

\- Pandas

\- NumPy

\- Scikit-learn

\- XGBoost

\- Matplotlib

\- Jupyter Notebook



\---



\## Current Status



\- ✅ Data Preprocessing Completed

\- ✅ Feature Engineering Completed

\- ✅ Data Preparation Completed

\- ✅ Model Training Completed

\- ✅ Model Evaluation Completed

\- ✅ Feature Importance Analysis Completed

\- ✅ Accuracy Validation Completed



\---



\## Future Work



\- Integrate the trained model with FastAPI

\- Develop a web dashboard for visualization

\- Add supply chain optimization recommendations

\- Deploy the complete application



\---



\## License



This project is developed for educational and research purposes.
\- XGBoost / LightGBM

\- FastAPI

\- React

\- Git \& GitHub



\## Project Status



🚧 Project setup completed. Development is in progress.

