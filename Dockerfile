FROM python:3.7

WORKDIR /app
COPY . .

RUN pip install pipenv
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "init.py"]
