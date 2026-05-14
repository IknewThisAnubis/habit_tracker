FROM python:3.11-slim
# avoid write compiled bytecode to __pycache__/ in the container
ENV PYTHONDONTWRITEBYTECODE=1 
# immediate log output 
ENV PYTHONUNBUFFERED=1

COPY .  /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]
