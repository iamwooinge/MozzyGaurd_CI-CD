import joblib

model = joblib.load('models/best_rf_model.pkl')

# 모델의 클래스 확인 (Optional)
print(f"Loaded model type: {type(model)}")
