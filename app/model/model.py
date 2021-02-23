import os
import pickle

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

MODEL_DIR = os.path.dirname(__file__)
MODEL_NAME = "DecisionTreeClassifier"

data = load_iris()
X_train = data.data
y_train = data.target
random_state = 0
min_samples_leaf = 3

model = DecisionTreeClassifier(random_state=random_state, min_samples_leaf=min_samples_leaf)
model.fit(X_train, y_train)

with open(os.path.join(MODEL_DIR, MODEL_NAME) + ".pickle", "wb") as file_:
    pickle.dump(model, file_, protocol=2)
