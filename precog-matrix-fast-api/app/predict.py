import joblib
import numpy as np
import lightgbm
import pandas as pd

    #primeiro passo: fazer o load do modelo (XGBOOST ou outro)
    #segundo passo: model.predict   (predict proba)
    #terceir opasso: retornar o output (prob)

model_path = 'models/crime_prediction_lightgbm_model.joblib'
onehot_columns = ['Crime_A', 'Crime_B', 'Crime_C', 'Crime_D', 'Crime_E', 'Crime_F']  # Tem que ajustar, pq não sei os nomes


def load_model(model_path):
    """Load the trained model from a file."""
    return joblib.load(model_path)

def predict(df_processed, model):

    """Make predictions using the loaded model."""
    # Ensure the model and input data are compatible
    if model is None:
        raise ValueError("Model is not loaded. Please load the model before predicting.")

    # Check if df_processed is a DataFrame or array-like structure
    if df_processed is None or len(df_processed) == 0:
        raise ValueError("The input data is empty or None.")

    # Make predictions (predict_proba returns the probability of each class)
    probabilities = model.predict_proba(df_processed)

    # Return the predicted probabilities
    return probabilities

def main(model_path, data, class_names):
    """Main function to load the model and make predictions."""
    # Carregar o modelo
    model = load_model(model_path)

    # Verificar se os dados estão no formato correto
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Data should be a pandas DataFrame.")

    # Fazer várias predições reutilizando o mesmo modelo carregado
    results = predict(data, model)

    #for i, prob in enumerate(results):
    #    print(f"Probabilities {i}: {prob}")

    return results
