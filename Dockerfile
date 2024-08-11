FROM python:3.10-alpine
WORKDIR /app
RUN pip install django 
RUN pip install kubernetes
RUN apk update && apk add --no-cache \
    curl \
    bash \
    ca-certificates \
    # Install kubectl
    && curl -LO "https://dl.k8s.io/release/v1.27.0/bin/linux/amd64/kubectl" \
    && chmod +x ./kubectl \
    && mv ./kubectl /usr/local/bin/kubectl \
    # Verify kubectl installation
    && kubectl version --client \
    # Clean up
    && apk del curl
COPY djangosrc/dashboard /app
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
CMD ["python", "manage.py", "runserver","0.0.0.0:8000"]
