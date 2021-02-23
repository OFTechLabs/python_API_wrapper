import os
import pickle

from fastapi import FastAPI
from pydantic import BaseModel
import mimetypes

from app.model.Flower import Flower


app = FastAPI(
    title="App deployment as a microservice",
    description="This project helps you to setup your Python application as a microservice, by hosting it"
                "in a Docker container, accessible through REST API.",
    version="0.1.0",
)

mimetypes.init()

file_path = os.path.dirname(__file__)
model_dir = os.path.join("model")
model_name = "DecisionTreeClassifier"
path = os.path.join(file_path, model_dir, model_name+".pickle")
model = pickle.load(open(path, "rb"))


class Input(BaseModel, Flower):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


class Output(BaseModel):
    predicted_class: int
    predicted_name: str


@app.get("/print_flower/", response_model=Input)
def print_flower() -> Input:
    flower = Input(sepal_length=1.0, sepal_width=2.0, petal_length=3.0, petal_width=4.0)
    print(flower)
    return flower


@app.post("/predict/", response_model=Output)
def predict(flower: Input) -> Output:
    return Output(predicted_class=flower.predict_class(model),
                  predicted_name=flower.predict_name(model))
