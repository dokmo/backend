FROM python:3.12
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./api /code/api
COPY ./core /code/core
COPY main.py /code/main.py

CMD ["python3", "main.py"]
