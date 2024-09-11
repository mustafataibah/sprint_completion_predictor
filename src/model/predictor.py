from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
from config import MODEL_FILE

class CompletionPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    def train(self, features_df):
        X = features_df[['estimate', 'day_of_week']]
        y = features_df['completion_time']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        
        predictions = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        print(f"Model Mean Absolute Error: {mae}")
    
    def predict(self, story_points, day_of_week):
        return self.model.predict([[story_points, day_of_week]])[0]
    
    def save_model(self):
        joblib.dump(self.model, MODEL_FILE)
    
    def load_model(self):
        self.model = joblib.load(MODEL_FILE)

if __name__ == "__main__":
    # For testing purposes
    from src.data_collection.linear_api import fetch_issues
    from src.data_collection.github_api import fetch_merged_prs
    from src.data_processing.preprocessor import preprocess_data
    
    issues = fetch_issues()
    prs = fetch_merged_prs()
    processed_data = preprocess_data(issues, prs)
    
    predictor = CompletionPredictor()
    predictor.train(processed_data)
    predictor.save_model()
    
    # Test prediction
    print(f"Predicted completion time: {predictor.predict(3, 2)} days")