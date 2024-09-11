from src.data_collection.linear_api import fetch_issues
from src.data_collection.github_api import fetch_merged_prs
from src.data_processing.preprocessor import preprocess_data
from src.model.predictor import CompletionPredictor

def main():
    print("Fetching data...")
    issues = fetch_issues()
    prs = fetch_merged_prs()
    
    print("Preprocessing data...")
    processed_data = preprocess_data(issues, prs)
    
    print("Training model...")
    predictor = CompletionPredictor()
    predictor.train(processed_data)
    predictor.save_model()
    
    print("Model trained and saved.")
    
    # Example prediction
    story_points = 3
    day_of_week = 2  # 0 = Monday, 6 = Sunday
    predicted_days = predictor.predict(story_points, day_of_week)
    print(f"A task with {story_points} story points started on day {day_of_week} is predicted to take {predicted_days:.2f} days.")

if __name__ == "__main__":
    main()