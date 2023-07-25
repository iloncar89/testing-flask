FROM python:3.11-slim-buster
COPY . /app
WORKDIR /app
RUN pip install -r req.txt
# CMD ["python3", "app.py"]
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "8085"]