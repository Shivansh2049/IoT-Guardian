# backend/ml/predict.py
import joblib, os
MODEL_PATH = "model.joblib"
def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    from train_model import train_and_save_model
    train_and_save_model()
    return joblib.load(MODEL_PATH)

def predict(features):
    model = load_model()
    X = [[features.get("port_count",0), features.get("avg_cvss",0), features.get("firmware_age",0), features.get("weak_creds",0), features.get("exploit_count",0)]]
    p = model.predict_proba(X)[0][1] if hasattr(model, "predict_proba") else float(model.predict(X)[0])
    return {"prob": float(p), "risk_score": round(p*10,2)}
