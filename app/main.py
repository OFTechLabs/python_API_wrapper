import uvicorn
import os
import pickle

from fastapi import FastAPI
from pydantic import BaseModel
import mimetypes

#from app.model.Flower import Flower


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


class Flower:
    flower_names = ["setosa", "versicolor", "virginica"]

    def __init__(self, sepal_length: float, sepal_width: float, petal_length: float, petal_width: float):
        self.sepal_length = sepal_length
        self.sepal_width = sepal_width
        self.petal_length = petal_length
        self.petal_width = petal_width

    def predict_class(self, model) -> int:
        return model.predict([[self.sepal_length,
                               self.sepal_width,
                               self.petal_length,
                               self.petal_width]])[0]

    def predict_name(self, model) -> str:
        return self.flower_names[self.predict_class(model)]

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
    uvicorn.run("main:app", host="127.0.0.1", port=80, log_level="info", reload=True)
