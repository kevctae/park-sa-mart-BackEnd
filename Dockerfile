FROM python:3.9.1
RUN apt-get update -y && apt-get install -y build-essential
COPY . /app
WORKDIR /app 
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]