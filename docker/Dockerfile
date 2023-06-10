FROM python:3.10

WORKDIR /code/app

COPY .env db.py main.py models.py requirements.txt schemas.py db_funcs.py /code/app/

RUN mkdir -p /code/app/temp

RUN apt-get update && apt-get install -y ffmpeg

RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt

RUN apt update && apt install nano iputils-ping -y

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

