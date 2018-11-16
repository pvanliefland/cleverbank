FROM python:3
COPY . /usr/src/app
WORKDIR /usr/src/app
CMD ["python", "report.py"]