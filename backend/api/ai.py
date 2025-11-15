from flask import Blueprint, jsonify, request
from ml.train_model import train_and_save_model
from ml.predict import predict

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/train", methods=["POST"])
def train():
    res = train_and_save_model()
    return jsonify(res)

@ai_bp.route("/predict", methods=["POST"])
def predict_route():
    features = request.json or {}
    result = predict(features)
    return jsonify(result)
