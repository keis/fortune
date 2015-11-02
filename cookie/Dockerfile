FROM python:3.4
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY cookie.py /cookie.py
CMD python /cookie.py
EXPOSE 8000
