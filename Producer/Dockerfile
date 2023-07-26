# producer/Dockerfile

FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /home/app

# Set the working directory to the "producer" folder
WORKDIR /home/app/producer

# Copy the contents of the "producer" folder into the container
COPY . /home/app/producer

RUN pip install -r requirements.txt

CMD ["uvicorn", "producer:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
