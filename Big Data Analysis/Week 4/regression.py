import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def root_relative_squared_error(y_true, y_pred):
    numerator = np.sum((y_true - y_pred) ** 2)
    denominator = np.sum((y_true - np.mean(y_true)) ** 2)
    return np.sqrt(numerator / denominator)
def relative_absolute_error(y_true, y_pred):
    numerator = np.sum(np.abs(y_true - y_pred))
    denominator = np.sum(np.abs(y_true - np.mean(y_true)))
    return numerator / denominator


df = pd.read_csv("Week 3/possum.csv", delimiter=",", encoding="utf-8")
df_dummy = pd.get_dummies(df)

target = "totalL"
features = ['site', 'sex_m', 'sex_f', 'age', 'headL', 'tailL', 
            'skullW']

X = df_dummy[features]
y = df_dummy[target]

X_train_lr, X_test_lr, y_train_lr, y_test_lr = train_test_split(
    X, y, test_size=0.4, random_state=42
)

linreg = LinearRegression()
linreg.fit(X_train_lr, y_train_lr)

y_preds_lr = linreg.predict(X_test_lr)

features_scaled = StandardScaler().fit_transform(X)
target_scaled = StandardScaler().fit_transform(y.values.reshape(-1, 1))
X_train_svr, X_test_svr, y_train_svr, y_test_svr = train_test_split(
    features_scaled, target_scaled, test_size=0.2, random_state=42
)

svrreg = SVR(kernel='rbf', C=1.0, epsilon=0.1)
svrreg.fit(X_train_svr, y_train_svr.ravel())

y_preds_svr = svrreg.predict(X_test_svr)


print('---------------- LR Model -----------------------------')
print("RRSE:", root_relative_squared_error(y_test_lr, y_preds_lr))
print("RAE:", relative_absolute_error(y_test_lr, y_preds_lr))
print("RMSE:", np.sqrt(mean_squared_error(y_test_lr, y_preds_lr)))
print("R² score:", r2_score(y_test_lr, y_preds_lr))
print('MSA:', mean_absolute_error(y_test_lr, y_preds_lr))
print('---------------- SVR Model -----------------------------')
print("RRSE:", root_relative_squared_error(y_test_svr, y_preds_svr))
print("RAE:", relative_absolute_error(y_test_svr, y_preds_svr))
print("RMSE:", np.sqrt(mean_squared_error(y_test_svr, y_preds_svr)))
print("R² score:", r2_score(y_test_svr, y_preds_svr))
print('MSA:', mean_absolute_error(y_test_svr, y_preds_svr))
