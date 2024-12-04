import joblib
model_file = '10ftag_prediction_model.pkl'
vectorizer_file = '10ftfidf_vectorizer.pkl'
mlb_file = '10fmlb.pkl'

model = joblib.load(model_file)
vectorizer = joblib.load(vectorizer_file)
mlb = joblib.load(mlb_file)

new_data = ["select","regex "]
new_data_tfidf = vectorizer.transform(new_data)
predicted_tags_binary = model.predict(new_data_tfidf)
predicted_tags = mlb.inverse_transform(predicted_tags_binary)
print(f'Predicted Tags: {predicted_tags}')