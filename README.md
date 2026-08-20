SupplyPrescript

Closed-Loop Prescriptive Analytics for Supply Chain Operations

SupplyPrescript is an end-to-end supply chain analytics system developed as part of a Data Analytics Internship project. The system combines data preprocessing, machine learning, operational risk prediction, prescriptive optimization, decision execution, write-back, evaluation, reporting, and deployment into one closed-loop workflow.

The final application supports:

Predict → Prescribe → Execute → Write Back → Evaluate → Report

The project began as a machine-learning risk-classification pipeline and evolved into a complete working application with a FastAPI backend, optimization engine, persistent decision records, an interactive frontend, CSV reporting, and Render deployment.

Project Status

Final Branch: main

Current Status: Completed and deployed

Completed

Data collection and cleaning

Feature engineering

Data preparation

Offline XGBoost risk-classification pipeline

Model evaluation and feature-importance analysis

Operational shipment-delay prediction model

FastAPI REST backend

SQLite database integration

Route and transport optimization

Decision execution and write-back

Decision evaluation

Dashboard analytics

Prediction interface

Prescription interface

Decision history

Reports and CSV export

Frontend/backend integration

End-to-end testing

Render deployment

Live Deployment

Backend API

https://supplyprescript-api.onrender.com

Health check:

https://supplyprescript-api.onrender.com/

Swagger API documentation:

https://supplyprescript-api.onrender.com/docs

Frontend

The frontend is deployed as a Render Static Site.

Replace this line with the exact frontend Render URL.

(https://supplyprescript-v2u9.onrender.com)

Render Free-Tier Note

The backend is deployed on Render's free tier. A free service may spin down after inactivity, so the first request after a period of inactivity can take additional time while the service wakes up.

The current backend uses SQLite. SQLite is suitable for this project demonstration, but Render's default filesystem is not intended for permanent production database persistence across every restart/redeploy. A production deployment should use PostgreSQL or another managed database.

1. Problem Statement

Modern supply chains are affected by:

shipment delays

severe weather

high traffic

route risk

supplier reliability

lead-time variation

inventory shortages

logistics cost

capacity constraints

disruption probability

Traditional dashboards often stop at descriptive or predictive analytics. They may show what happened or what is likely to happen, but they do not always recommend an operational action and track whether the action actually worked.

SupplyPrescript was designed to move beyond prediction.

The system answers three operational questions:

What is likely to happen?

What action should be taken?

Did the selected action perform as expected?

2. Project Objective

The objective of SupplyPrescript is to build a closed-loop prescriptive analytics system for supply chain operations.

The system:

predicts shipment delay/risk

identifies high-risk shipments

recommends alternative transport options

compares cost, time, and residual risk

allows an operator to execute a recommendation

stores the decision in the database

records actual cost and time later

compares actual results against expected results

generates decision-performance reports

exports decision data as CSV

3. End-to-End Workflow

Raw Supply Chain Dataset
          │
          ▼
Data Preprocessing
          │
          ▼
Feature Engineering
          │
          ▼
Data Preparation
          │
          ▼
Offline ML Training & Evaluation
          │
          ▼
Operational Prediction Model
          │
          ▼
FastAPI Prediction API
          │
          ▼
Frontend Prediction Interface
          │
          ▼
Optimization / Prescription Engine
          │
          ▼
Operator Executes Decision
          │
          ▼
Decision Written to Database
          │
          ▼
Actual Cost / Time Evaluation
          │
          ▼
Outcome Classification
          │
          ▼
Dashboard / Reports / CSV Export

4. Repository Structure

SupplyPrescript/
│
├── backend/
│   └── app/
│       ├── models/
│       ├── routers/
│       ├── schemas/
│       ├── services/
│       ├── database.py
│       └── main.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   └── TEAM_GUIDE.md
│
├── frontend/
│   ├── index.html
│   ├── src/
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── models/
│   ├── xgboost_model.pkl
│   ├── delay_model.joblib
│   └── train_delay_model.py
│
├── notebooks/
├── optimization/
│   └── optimizer.py
├── optimization_engine/
│   └── optimization_engine.py
├── reports/
├── src/
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── data_preparation.py
│   ├── model_training.py
│   └── model_evaluation.py
├── requirements.txt
└── README.md

5. Dataset

The original machine-learning pipeline uses a supply-chain logistics dataset.

Item

Value

Total records

113,097

Original features

18

Features after cleaning

16

Features after engineering

20

Offline target

risk_classification

The preprocessing pipeline removes:

product_id

supplier_id

and retains operational supply-chain variables such as inventory level, handling-equipment availability, fulfillment status, weather severity, shipping cost, supplier reliability, lead time, historical demand, cargo condition, route risk, customs time, disruption likelihood, delay probability, delivery deviation, and supplier country.

6. Data Preprocessing

File:

src/preprocessing.py

The preprocessing stage performs:

raw dataset loading

unnecessary-column removal

missing-value checks

target-variable encoding

cleaned-dataset generation

Output:

data/processed/cleaned_supply_chain.csv

7. Feature Engineering

File:

src/feature_engineering.py

Four business-oriented engineered features were created.

Feature

Formula / Meaning

inventory_coverage

warehouse_inventory_level / (historical_demand + 1)

supplier_efficiency

supplier_reliability_score / (lead_time_days + 1)

logistics_risk

shipping_costs × route_risk_level

delay_impact

delay_probability × delivery_time_deviation

Additional checks include duplicate detection, missing-value validation, and summary statistics.

Output:

data/processed/feature_engineered_supply_chain.csv

8. Data Preparation

File:

src/data_preparation.py

The data-preparation stage performs:

loading of the engineered dataset

one-hot encoding of supplier_country

feature/target separation

stratified train/test split

80:20 train/test ratio

random_state=42

Generated artifacts include:

X_train.csv
X_test.csv
y_train.csv
y_test.csv

9. Machine Learning Architecture

SupplyPrescript currently contains two ML paths serving different purposes.

9.1 Offline XGBoost Risk-Classification Pipeline

Files:

src/model_training.py
src/model_evaluation.py
models/xgboost_model.pkl

Algorithm:

XGBoost Classifier

Main parameters:

n_estimators = 100
max_depth = 6
learning_rate = 0.1
random_state = 42
objective = multi:softmax

The offline pipeline predicts:

risk_classification

Recorded Evaluation

Metric

Score

Accuracy

99.99%

Precision

99.99%

Recall

99.99%

F1 Score

99.99%

The evaluation pipeline also generates a classification report, confusion matrix, and feature-importance analysis.

Important Validation Finding

disruption_likelihood_score was found to be an extremely strong predictor.

When this feature was removed in a validation experiment, accuracy dropped to approximately:

75.15%

Therefore, the 99.99% result should be interpreted cautiously because disruption_likelihood_score may behave as a near-target proxy or introduce information leakage.

9.2 Live Operational Delay Prediction Model

The deployed FastAPI application currently uses:

models/delay_model.joblib

Training script:

models/train_delay_model.py

Model:

RandomForestClassifier

The live model accepts:

distance

weather

traffic

vehicle type

The model is loaded by:

backend/app/services/ml_service.py

The prediction service first attempts model inference. If the model artifact cannot be loaded, the backend contains a deterministic fallback risk calculation so the API can still return an operational result.

Important Clarification

The deployed frontend's shipment-delay predictions currently use delay_model.joblib.

The offline xgboost_model.pkl remains part of the project's risk-classification research pipeline.

These two model artifacts should not be presented as the same model or directly compared because they were built for different data/targets.

10. Prediction Service

Frontend Form
     │
     ▼
POST /api/v1/predictions/
     │
     ▼
FastAPI
     │
     ▼
ML Service
     │
     ▼
Prediction + Probability + Recommendation
     │
     ▼
SQLite Write-Back
     │
     ▼
Frontend Table / Dashboard

Each stored prediction includes shipment ID, origin, destination, distance, weather, traffic, vehicle type, prediction, probability, recommendation, and timestamp.

Shipment IDs use the form:

SHP-XXXXXXXX

11. Prescriptive Optimization

The live application uses:

optimization/optimizer.py

through:

POST /api/v1/optimization/simulate

The optimizer compares:

Truck

Express Truck

Container

Air Freight

Rail Logistics

For each mode it estimates:

cost

travel time

residual risk

whether it is the current mode

The optimizer considers distance, weather, traffic, vehicle type, and urgency level.

The result identifies an optimal mode and returns all alternatives for comparison.

12. PuLP Optimization Prototype

The repository also contains:

optimization_engine/optimization_engine.py

This is a separate PuLP-based optimization prototype containing business options such as Air Freight, Secondary Supplier, and Delay Launch, with constraints such as budget and maximum delay.

Important Clarification

The current deployed /api/v1/optimization/simulate endpoint is connected to the route optimizer in:

optimization/optimizer.py

The separate PuLP prototype exists in the repository but is not currently the solver directly called by the deployed endpoint.

13. FastAPI Backend

Backend entry point:

backend/app/main.py

Framework:

FastAPI

Features:

REST API

Swagger documentation

CORS middleware

SQLAlchemy integration

prediction service

analytics service

optimization service

decision service

report service

model-status service

Local backend:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs

14. Main API Endpoints

Predictions

POST /api/v1/predictions/
GET  /api/v1/predictions/?skip=0&limit=20
GET  /api/v1/predictions/{prediction_id}
GET  /api/v1/predictions/shipment/{shipment_id}

Example create request:

{
  "origin": "Mumbai",
  "destination": "Delhi",
  "distance": 1400,
  "weather": "Storm",
  "traffic": "High",
  "vehicle_type": "Container"
}

Optimization

POST /api/v1/optimization/simulate
GET  /api/v1/optimization/modes

Decisions

POST /api/v1/decisions/execute
POST /api/v1/decisions/{decision_id}/evaluate
GET  /api/v1/decisions
GET  /api/v1/decisions/analytics

Example evaluation:

{
  "actual_cost": 10500,
  "actual_hours": 7.5
}

Analytics

GET  /api/v1/analytics/summary
GET  /api/v1/analytics/breakdown
POST /api/v1/predictions/batch

Reports

POST /api/v1/reports/upload-csv
GET  /api/v1/reports/export-csv

15. Database and Write-Back

The current implementation uses:

SQLite

with SQLAlchemy.

Database configuration:

backend/app/database.py

The database stores:

shipment predictions

executed operational decisions

evaluated outcomes

The write-back process allows the system to preserve the operational decision rather than only displaying a recommendation.

16. Decision Evaluation

After execution, a decision initially has:

Status: Executed
Actual Cost: null
Actual Hours: null
Actual Outcome: null

The operator later provides real operational results.

The backend classifies outcomes as:

Better Than Expected

actual_cost <= selected_cost
AND
actual_hours <= selected_hours

Worse Than Expected

actual_cost > selected_cost
AND
actual_hours > selected_hours

Mixed Outcome

One metric improves while the other becomes worse.

After evaluation:

Status: Evaluated

and the outcome is stored.

17. Frontend

The final frontend is served through Vite.

Main file:

frontend/index.html

The repository retains React/Vite source scaffolding, but the final integrated operational interface is implemented in the main HTML entry point using:

HTML

CSS

JavaScript

Fetch API

Vite

The frontend contains five main views.

Dashboard

Displays shipment totals, delayed shipments, high-risk shipments, decisions, risk distribution, recent decisions, and pipeline status.

Predictions

Accepts origin, destination, distance, weather, traffic, and vehicle type, then calls the real FastAPI prediction endpoint.

Prescriptions

Calls the optimization API and displays alternative transport modes with expected cost, time, residual risk, and the recommended mode.

Decisions

Displays shipment, selected recommendation, expected values, actual values, verdict, and evaluation status.

Reports

Displays outcome distribution, pending/evaluated decisions, expected vs actual cost, performance summary, and supports CSV export.

18. Closed-Loop Architecture

┌─────────────┐
│   PREDICT   │
└──────┬──────┘
       ▼
┌─────────────┐
│  PRESCRIBE  │
└──────┬──────┘
       ▼
┌─────────────┐
│   EXECUTE   │
└──────┬──────┘
       ▼
┌─────────────┐
│ WRITE BACK  │
└──────┬──────┘
       ▼
┌─────────────┐
│  EVALUATE   │
└──────┬──────┘
       ▼
┌─────────────┐
│   REPORT    │
└─────────────┘

19. Local Installation

Clone

git clone https://github.com/hissainikhalid-oss/axlero-data-analyst-team48.git
cd axlero-data-analyst-team48

Backend

pip install -r requirements.txt
cd backend
python -m uvicorn app.main:app --reload

Backend:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs

Frontend

Open another terminal:

cd frontend
npm install
npm run dev

Frontend:

http://localhost:5173

Local frontend calls:

http://127.0.0.1:8000

Deployed frontend calls:

https://supplyprescript-api.onrender.com

20. Render Deployment

The application is deployed using two Render services.

Backend Web Service

Repository:

hissainikhalid-oss/axlero-data-analyst-team48

Branch:

main

Root directory:

Leave empty

Build command:

pip install -r requirements.txt

Start command:

cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT

Backend:

https://supplyprescript-api.onrender.com

Frontend Static Site

Branch:

main

Root directory:

frontend

Build command:

npm install && npm run build

Publish directory:

dist

The frontend switches automatically between local FastAPI and the Render API based on hostname.

21. Testing Performed

Prediction Test

created shipment from frontend

received ML prediction

received delay probability

verified record appeared in prediction table

verified backend persistence

Optimization Test

selected delayed/high-risk shipment

clicked PRESCRIBE

verified optimization response

displayed transport alternatives

verified optimal option highlighting

Decision Test

executed a selected mode

verified database write-back

verified Decisions page

hard-refreshed application

verified record persisted through backend reload

Evaluation Test

entered actual cost

entered actual completion time

backend evaluated result

verified verdict and Evaluated status

Reporting Test

verified outcome counts

verified expected vs actual values

verified pending/evaluated decisions

tested CSV export

Deployment Test

deployed FastAPI backend to Render

verified health endpoint

verified Swagger

deployed frontend as Render Static Site

verified deployed frontend/backend communication

22. Example User Journey

1. Open Predictions
2. Enter shipment details
3. Run Prediction
4. Prediction is stored in backend
5. Click PRESCRIBE
6. Optimization evaluates transport alternatives
7. Review cost, time, and residual risk
8. Execute selected option
9. Decision is written to database
10. Enter actual cost/time later
11. Backend classifies outcome
12. Reports refresh
13. Export decision data as CSV

23. Technology Stack

Data / ML

Python

Pandas

NumPy

Scikit-learn

XGBoost

Joblib

Jupyter Notebook

Matplotlib

Optimization

Python

custom route optimization

PuLP

SciPy

Backend

FastAPI

Uvicorn

Pydantic

SQLAlchemy

SQLite

Frontend

HTML

CSS

JavaScript

Fetch API

Vite

Development / Deployment

Git

GitHub

Render

24. Team Workflow

The project used a branch-based Git workflow.

Team Leader / ML & Integration

dataset

preprocessing

feature engineering

machine-learning pipeline

model evaluation

integration

merging

final testing

deployment coordination

Optimization

optimization logic

operational recommendations

transport alternatives

business constraints

Backend / Dashboard

FastAPI

database

write-back APIs

dashboard/frontend work

The final integrated and deployed project is maintained on:

main

Other branches may remain as development or backup history.

25. Known Limitations

SQLite on Render

SQLite is suitable for development and demonstration, but a production cloud deployment should use PostgreSQL or another managed database.

Free Render Cold Start

The backend may require additional startup time after inactivity.

Offline and Live ML Models Differ

The XGBoost risk-classification pipeline and live Random Forest delay model solve different tasks. Their metrics should not be directly compared without retraining candidate algorithms using the same target, dataset, preprocessing, and split.

XGBoost Accuracy / Leakage Risk

The extremely high XGBoost score is strongly associated with disruption_likelihood_score. The validation experiment suggests the variable may contain near-target information.

PuLP Integration

A PuLP prototype exists, but the deployed optimization endpoint currently uses the route optimizer rather than directly invoking the PuLP solver.

Continuous Retraining

The system supports outcome evaluation and reporting. Fully automatic model retraining from evaluated decisions is a future enhancement and should not be presented as already implemented.

26. Future Improvements

PostgreSQL deployment

authentication and role-based access

automated retraining

model registry/versioning

Random Forest vs XGBoost vs LightGBM benchmark on the same target

real logistics APIs

weather and traffic APIs

supplier database integration

direct PuLP solver integration into the live API

configurable budget/capacity constraints

model monitoring and drift detection

CI/CD tests

Docker

notifications

downloadable PDF reports

27. Final Result

SupplyPrescript evolved from a standalone machine-learning experiment into a working closed-loop prescriptive analytics application.

The final system combines:

Data
+
Machine Learning
+
FastAPI
+
Optimization
+
Operational Decision Making
+
Database Write-Back
+
Outcome Evaluation
+
Reporting
+
Cloud Deployment

Rather than only predicting risk, the application helps an operator select an action, records that action, measures the result, and reports whether the operational decision performed better or worse than expected.

28. Repository

https://github.com/hissainikhalid-oss/axlero-data-analyst-team48

Final branch:

main

29. License

This project was developed for educational, internship, demonstration, and research purposes.

SupplyPrescript

Closed-Loop Prescriptive Analytics for Supply Chain Operations

Predict → Prescribe → Execute → Write Back → Evaluate → Report
