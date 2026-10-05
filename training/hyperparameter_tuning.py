def run_hyperparameter_tuning_report():
    """
    Summarizes hyperparameter configurations for the four trained production models.
    """
    print("--- SynthSoma Fitted Model Hyperparameter Audit ---")
    print("1. Disease Model Ensemble: K-Nearest Neighbors (metric='cosine', n_neighbors=3-5), Random Forest (n_estimators=100)")
    print("2. Medicine Model: MultiOutputClassifier with LogisticRegression / SGD, TF-IDF ngram_range=(1,2)")
    print("3. Precaution Model: MultiOutputClassifier with DecisionTree/RF, TF-IDF ngram_range=(1,2)")
    print("4. Risk Factor Model: NearestNeighbors (metric='cosine', n_neighbors=1), TF-IDF char_wb ngram_range=(2,4)")

if __name__ == '__main__':
    run_hyperparameter_tuning_report()
