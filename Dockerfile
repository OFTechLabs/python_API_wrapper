FROM python:3.7

COPY requirements.txt /project/

RUN apt-get update \
 && pip install --upgrade pip \
 && pip install -r /project/requirements.txt

COPY app /project/app

WORKDIR /project

EXPOSE 80
#CMD [ "python", "./app/main.py" ]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]