FROM python:3.9.1
RUN apt-get update -y && apt-get install -y build-essential
COPY . /app
WORKDIR /app 
ENV TZ=Asia/Bangkok
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]