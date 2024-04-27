FROM python:3.9.4
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY static /app/static
COPY templates /app/templates
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY *.py /app
ENTRYPOINT ["python3", "web.py"]