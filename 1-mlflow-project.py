import mlflow
import mlflow.sklearn
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import os

# Load the iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# MLFLOW_TRACKING_URI = "ADD YOUR TRACKING URI HERE"
# mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# os.environ["MLFLOW_TRACKING_USERNAME"] = "ADD YOUR USERNAME HERE"
# os.environ["MLFLOW_TRACKING_PASSWORD"] = "ADD YOUR PASSWORD HERE"

# Set the MLflow experiment name
mlflow.set_experiment("Iris Classification v1")

# Start an MLflow run
with mlflow.start_run(run_name="Random Forest Classifier"):
    # Define model parameters
    params = {
        "n_estimators": 50,
        "max_depth": 2,
        "random_state": 42
    }
    
    # Log parameters
    mlflow.log_params(params)
    
    # Train the model
    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    # Log metrics
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1_score", f1)
    
    # Log the model
    mlflow.sklearn.log_model(model, "iris_model")
    
    # Log some example predictions
    example_predictions = {
        "predictions": y_pred.tolist()[:5],
        "true_values": y_test.tolist()[:5]
    }
    mlflow.log_dict(example_predictions, "example_predictions.json")
    
    print(f"Model accuracy: {accuracy:.4f}")
    print(f"Model precision: {precision:.4f}")
    print(f"Model recall: {recall:.4f}")
    print(f"Model F1 score: {f1:.4f}")
    print("\nMLflow run completed. You can view the results in the MLflow UI.")
