import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

np.random.seed(42)

# Generate 200 rows of 20 binary features
n_rows = 200
n_features = 20

X = np.random.randint(0, 2, size=(n_rows, n_features))
columns = [f"F{i + 1}" for i in range(n_features)]
df = pd.DataFrame(X, columns=columns)

# Define a label: based on parity of F1 + F2 + F3 plus noise
noise = np.random.binomial(1, 0.1, size=n_rows)  # 10% noise
df["Label"] = ((df["F1"] + df["F2"] + df["F3"]) % 2) ^ noise

# Save to CSV
file_path = "Week 2/larger_dataset.csv"
df.to_csv(file_path, index=False)


df = pd.read_csv("Week 2/larger_dataset.csv")  # Replace with your filename
X = df.drop(columns=["Label"])
y = df["Label"]

model = DecisionTreeClassifier()
k_folds = 5
max_features = X.shape[1]
min_gain = 0.005


def race_forward_selection(X, y, model, k_folds=5, min_gain=0.005):
    selected_features = []
    remaining_features = list(X.columns)
    current_score = 0.0

    while remaining_features and len(selected_features) < max_features:
        # Each iteration is a race
        best_feature = None
        best_score = current_score

        for feature in remaining_features:
            trial_features = selected_features + [feature]
            trial_X = X[trial_features]

            # Perform stratified k-fold cross-validation
            scores = []
            skf = StratifiedKFold(n_splits=k_folds, shuffle=True, random_state=42)
            for train_idx, test_idx in skf.split(trial_X, y):
                model.fit(trial_X.iloc[train_idx], y.iloc[train_idx])
                preds = model.predict(trial_X.iloc[test_idx])
                scores.append(accuracy_score(y.iloc[test_idx], preds))

                # Early termination (race idea): stop if mean can't beat current best
                if np.mean(scores) + (1.0 / len(scores)) * 0.1 < best_score:
                    break

            avg_score = np.mean(scores)

            if avg_score > best_score:
                best_feature = feature
                best_score = avg_score

        # If no feature improved performance enough, stop
        if best_score - current_score < min_gain:
            break

        selected_features.append(best_feature)
        remaining_features.remove(best_feature)
        current_score = best_score
        print(f"Selected: {best_feature} | Score: {best_score:.4f}")

    return selected_features, current_score


selected, score = race_forward_selection(
    X, y, model, k_folds=k_folds, min_gain=min_gain
)
print("\nFinal Selected Features:", selected)
print("Final Accuracy:", round(score, 4))
