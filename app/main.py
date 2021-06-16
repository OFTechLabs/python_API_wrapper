import os
import pickle

from fastapi import FastAPI
from pydantic import BaseModel
import mimetypes

app = FastAPI(
    title="App deployment as a microservice",
    description="This project helps you to setup your Python application as a microservice, by hosting it"
                "in a Docker container, accessible through REST API.",
    version="0.1.0",
)

mimetypes.init()

FILE_PATH = os.path.dirname(__file__)
MODEL_DIR = os.path.join("model")
MODEL_NAME = "DecisionTreeClassifier"
PATH = os.path.join(FILE_PATH, MODEL_DIR, MODEL_NAME + ".pickle")
model = pickle.load(open(PATH, "rb"))
flower_labels_to_names = {0: "setosa", 1: "versicolor", 2: "virginica"}


class Flower(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


class PredictedFlower(BaseModel):
    label: int
    name: str


@app.get("/sample_flower/", response_model=Flower)
def print_flower() -> Flower:
    flower = Flower(sepal_length=1.0, sepal_width=2.0, petal_length=3.0, petal_width=4.0)
    return flower


@app.post("/predict/", response_model=PredictedFlower)
def predict(flower: Flower) -> PredictedFlower:
    flower_label = model.predict([[flower.sepal_length,
                                   flower.sepal_width,
                                   flower.petal_length,
                                   flower.petal_width]])[0]
    flower_name = flower_labels_to_names[flower_label]
    return PredictedFlower(label=flower_label,
                           name=flower_name)
