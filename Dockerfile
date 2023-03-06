FROM debian
RUN apt update; apt upgrade -y; apt install -y python3 python3-dev python3-pip

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
ENV FLASK_APP=psunote/app.py
ENV FLASK_ENV=development

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0"]

