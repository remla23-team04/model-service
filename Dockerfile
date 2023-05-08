# Base image
FROM python:3.8-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Let other containers access the server at port 5000
EXPOSE 5000
# Copy over to container
COPY . .
# Run flask server
CMD [ "python", "./src/model-service.py" ]
