FROM apache/airflow:2.7.1-python3.10

USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories with proper permissions
RUN mkdir -p /opt/airflow/logs /opt/airflow/dags /opt/airflow/plugins && \
    chown -R airflow:root /opt/airflow && \
    chmod -R 775 /opt/airflow

USER airflow

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Make init script executable
USER root
RUN chmod +x /opt/airflow/docker/init-airflow.sh
USER airflow

# Set environment variables
ENV PYTHONPATH=/opt/airflow
ENV AIRFLOW_HOME=/opt/airflow
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
ENV AIRFLOW__CORE__FERNET_KEY=46BKJoQYlPPOexq0OhDZnIlNepKFf87WFwLbfzqDDho=
ENV AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=true 