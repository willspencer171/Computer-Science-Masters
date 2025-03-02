from neural_network_better import *
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Load data
digits = load_digits()
X, y = digits.data, digits.target

# Preprocess the data (e.g. scaling)
oh_enc = OneHotEncoder(sparse_output=False)
y = oh_enc.fit_transform(y.reshape(-1, 1))

scaler = StandardScaler()
X = scaler.fit_transform(X)

X = X.reshape((-1, 1, 8, 8))

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=43)

network = NeuralNetwork()

# Network architecture
network.add(ConvLayer((1, 8, 8), 3, 16))

network.add(ReLU())
network.add(FlattenLayer())
network.add(FullyConnected(16*8*8, 10))
network.add(Softmax())

network.fit(X_train, y_train, 
            CrossEntropyLoss(reg_method='l1', lambda_regularisation=0.001),
            SGD(learning_rate=.0001, batch_size=256),
            num_epochs=500)

loss, preds = network.evaluate(X_test, y_test)

from matplotlib import pyplot as plt

# Multi-class case
predicted_classes = np.argmax(preds, axis=1)
actual_classes = np.argmax(y_test, axis=1) if len(y_test.shape) > 1 else y_test

# Create confusion matrix
from sklearn.metrics import confusion_matrix
import seaborn as sns

cm = confusion_matrix(actual_classes, predicted_classes)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

""" fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.plot(pd.Series(network.losses))
ax1.set_ylabel('Loss')
ax1.set_xlabel('Epoch')
ax1.set_title(f'{network.loss}, {network.optimiser},\n{network.num_epochs} epochs')

ax2.scatter(y_test, preds)

plt.show()
 """