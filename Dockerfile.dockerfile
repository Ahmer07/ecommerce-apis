FROM python:3.8
WORKDIR /apis
COPY requirements.txt /apis

# UPDATE APT-GET
RUN apt-get update

# UPGRADE pip3
RUN pip3 install --upgrade pip

RUN pip install -r requirements.txt
COPY . /apis
CMD ["python", "./manage.py", "runserver", "0.0.0.0:80"]
EXPOSE 80

