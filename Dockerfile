FROM python:3.10.2-alpine3.15

WORKDIR /usr/src/app

COPY . .

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
