FROM python:3.11-rc-bullseye

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
