FROM python:3.9.1
RUN apt-get update -y && apt-get install -y build-essential
COPY . /app
WORKDIR /app 
RUN pip install -r requirements.txt
ENV TZ=Asia/Bangkok
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ENTRYPOINT ["python"]
CMD ["app.py"]
