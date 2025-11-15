# backend/ml/train_model.py
import numpy as np, joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

MODEL_PATH = "model.joblib"

def train_and_save_model():
    rng = np.random.RandomState(42)
    n=2000
    X = np.zeros((n,5))
    X[:,0] = rng.poisson(2,n)
    X[:,1] = rng.uniform(0,10,n)
    X[:,2] = rng.uniform(0,48,n)
    X[:,3] = rng.binomial(1,0.15,n)
    X[:,4] = rng.poisson(0.2,n)
    y = ((0.4*X[:,0] + 0.3*(X[:,1]/10) + 0.2*(X[:,2]/48) + 0.8*X[:,3] + 0.6*X[:,4]) > 1.0).astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42)
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    joblib.dump(rf, MODEL_PATH)
    return {"model_path": MODEL_PATH}
