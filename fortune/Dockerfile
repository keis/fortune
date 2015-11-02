FROM python:3.4
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY fortune.py fortune.sh /
CMD /fortune.sh
EXPOSE 8000
