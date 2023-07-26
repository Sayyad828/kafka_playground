# consumer/Dockerfile

FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /home/app

# Set the working directory to the "consumer" folder
WORKDIR /home/app/consumer

# Copy the contents of the "consumer" folder into the container
COPY . /home/app/consumer

RUN pip install -r requirements.txt

CMD ["uvicorn", "consumer:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
