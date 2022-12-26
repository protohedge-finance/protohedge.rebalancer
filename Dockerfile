
FROM python:3.10

WORKDIR /app

COPY requirements.txt  .
RUN pip3 install -r requirements.txt

# Copy function code
COPY . ./

CMD [ "python3", "main.py" ]


