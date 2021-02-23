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