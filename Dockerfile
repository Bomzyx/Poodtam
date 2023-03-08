FROM debian:sid
RUN echo 'deb http://mirror.psu.ac.th/debian/ sid main contrib non-free' > /etc/apt/sources.list
RUN apt update && apt upgrade -y
RUN apt install -y python3 python3-dev python3-pip python3-venv npm locales

RUN sed -i '/th_TH.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG th_TH.UTF-8 
ENV LANGUAGE th_TH:en 
ENV LC_ALL th_TH.UTF-8

COPY . /app
WORKDIR /app

RUN python3 -m venv /venv
ENV PYTHON=/venv/bin/python

RUN $PYTHON -m pip install flask gunicorn
RUN $PYTHON setup.py develop

RUN npm install --prefix poodtam/web/static

ENV POODTAM_SETTINGS=/app/poodtam.cfg

CMD ["/venv/bin/gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "poodtam.web:create_app()"]