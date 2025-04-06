# Ticker Sentiment Analysis

This project implements two Airflow pipelines for analyzing financial news sentiment and movie ratings data.

## Project Structure

```
Ticker-Sentiment-Analysis/
├── airflow/              # Airflow configuration and DAGs
├── src/                  # Source code
├── tests/               # Test files
├── docker/              # Docker configuration
└── scripts/             # Utility scripts
```

## Features

### Pipeline 1: Financial News Analysis
- Scrapes news from yourstory.com and finshots.in
- Processes articles related to HDFC and Tata Motors
- Generates sentiment scores
- Runs daily at 7 PM on working days

### Pipeline 2: MovieLens Analysis
- Processes MovieLens 100k dataset
- Runs daily at 8 PM on working days (after Pipeline 1)
- Performs various movie rating analyses

## Prerequisites

- Docker
- Docker Compose
- Python 3.10+

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Ticker-Sentiment-Analysis
```

2. Run the setup script:
```bash
./scripts/setup.sh
```

3. Access Airflow UI:
- URL: http://localhost:8080
- Username: admin
- Password: admin

## Development

### Running Tests
```bash
docker-compose -f docker/docker-compose.yml exec airflow-webserver pytest
```

### Adding New Dependencies
1. Add the dependency to `requirements.txt`
2. Rebuild the containers:
```bash
docker-compose -f docker/docker-compose.yml build
```
