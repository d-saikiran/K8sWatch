FROM python:3.10-alpine
WORKDIR /app
RUN pip install django 
RUN pip install kubernetes
COPY djangosrc/dashboard /app
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
CMD ["python", "manage.py", "runserver","0.0.0.0:8000"]
