from sklearn.datasets import load_iris, load_wine
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

import seaborn as sns
import matplotlib.pyplot as plt

data = load_wine()
test_sizes = [0.2, 0.3, 0.355, 0.4, 0.5]
fig, axes = plt.subplots(3, len(test_sizes), figsize=(10, 6), sharex=True, sharey=True)

for i, test_size in enumerate(test_sizes):
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=test_size, random_state=42)

    clf_tree = DecisionTreeClassifier(random_state=42)
    clf_tree.fit(X_train, y_train)

    y_pred_tree = clf_tree.predict(X_test)

    print("Decision Tree Classifier")
    print(classification_report(y_test, y_pred_tree, target_names=data.target_names))
    
    sns.heatmap(confusion_matrix(y_test, y_pred_tree), square=True, yticklabels=data.target_names, annot=True, fmt='d', cmap='Blues', ax=axes[0, i])

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    clf_svc = SVC(kernel='linear', random_state=42)
    clf_svc.fit(X_train_scaled, y_train)

    y_pred_svc = clf_svc.predict(scaler.transform(X_test))

    print("Support Vector Classifier")
    print(classification_report(y_test, y_pred_svc, target_names=data.target_names))
    sns.heatmap(confusion_matrix(y_test, y_pred_svc), square=True, yticklabels=data.target_names, annot=True, fmt='d', cmap='Blues', ax=axes[1, i])

    clf_nb = GaussianNB()
    clf_nb.fit(X_train, y_train)

    y_pred_nb = clf_nb.predict(X_test)

    print("Naïve Bayes Classifier")
    print(classification_report(y_test, y_pred_nb, target_names=data.target_names))
    sns.heatmap(confusion_matrix(y_test, y_pred_nb), square=True, yticklabels=data.target_names, xticklabels=data.target_names, annot=True, fmt='d', cmap='Blues', ax=axes[2, i])

model_names = ["Decision Tree", "Support Vector Classifier", "Naïve Bayes"]
for ax, model in zip(axes[:, 0], model_names):
    ax.set_ylabel(model, rotation=90, fontsize=12, labelpad=10)

# Set column labels (test sizes)
for ax, test_size in zip(axes[0], test_sizes):
    ax.set_title(f"Test size = {test_size * 100:.1f}%", fontsize=12)

plt.tight_layout()
plt.show()
