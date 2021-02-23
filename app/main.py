from typing import List, Optional, Dict
import uvicorn
import os
import pickle

from fastapi import FastAPI, Body
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
MODEL_DIR = os.path.join("model")
MODEL_NAME = "DecisionTreeClassifier"
path = os.path.join(file_path, MODEL_DIR, MODEL_NAME + ".pickle")

model = pickle.load(open(path, "rb"))


class Input(BaseModel, Flower):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


class Output(BaseModel):
    predicted_class: int
    predicted_name: str


@app.post("/result/", response_model=Output)
def predict(flower: Input) -> Output:
    return Output(predicted_class=flower.predict_class(model),
                  predicted_name=flower.predict_name(model))


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info", reload=True)
