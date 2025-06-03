import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv("Week 3/possum.csv", delimiter=",", encoding="utf-8")

target = "tailL"

X = df[[target]]
y = df["headL"]

model = LinearRegression()
model.fit(X, y)
print(f"Coefficient: {model.coef_[0]}")
print(f"Intercept: {model.intercept_}")
print(f"R^2: {model.score(X, y)}")

test_data = pd.DataFrame({target: [100, 150, 200]})
predictions = model.predict(test_data)
print(predictions)
