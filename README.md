# Ticker Sentiment Analysis

This project scrapes financial news from Finshots and YourStory, performs sentiment analysis on the articles, and stores the results in a PostgreSQL database. The pipeline is orchestrated using Apache Airflow.

## Prerequisites

- Docker
- Docker Compose

## Project Structure

```
.
├── airflow/
│   ├── dags/                    # Airflow DAGs
│   ├── data/                    # Temporary data storage
│   └── logs/                    # Airflow logs
├── docker/
│   ├── Dockerfile              # Docker configuration
│   └── docker-compose.yml      # Docker Compose configuration
├── src/
│   └── scrapers/               # Web scraping modules
└── requirements.txt            # Python dependencies
```

## Setup and Running

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Ticker-Sentiment-Analysis
   ```

2. **Create necessary directories**
   ```bash
   mkdir -p airflow/data airflow/logs
   ```

3. **Build and start the containers**
   ```bash
   docker-compose -f docker/docker-compose.yml up --build -d
   ```

4. **Access Airflow Web Interface**
   - Open your browser and go to `http://localhost:8080`
   - Login credentials:
     - Username: `admin`
     - Password: `admin`

5. **Start the Pipeline**
   - In the Airflow web interface, find the `ticker_sentiment_analysis` DAG
   - Click the play button (▶️) to trigger the DAG manually
   - The DAG will also run automatically at 7 PM every working day (Monday to Friday)

## Pipeline Workflow

The pipeline consists of the following steps:

1. **Parallel Scraping**
   - Scrapes latest articles from Finshots
   - Scrapes latest articles from YourStory

2. **Data Cleaning**
   - Cleans and standardizes the scraped data
   - Removes duplicates

3. **Sentiment Analysis**
   - Performs sentiment analysis on the combined dataset
   - Stores results in PostgreSQL database

### Pipeline 2: MovieLens Analysis
- Processes MovieLens 100k dataset
- Runs daily at 8 PM on working days (after Pipeline 1)
- Performs various movie rating analyses

## Monitoring

- **Airflow UI**: Monitor DAG runs, task status, and logs at `http://localhost:8080`
- **Logs**: View detailed logs in the Airflow UI or in the `airflow/logs` directory
- **Results**: Find processed data in:
  - CSV files in `airflow/data/`
  - PostgreSQL database (accessible through Airflow)

## Stopping the Pipeline

To stop the containers:
```bash
docker-compose -f docker/docker-compose.yml down
```

To stop and remove all data (including the database):
```bash
docker-compose -f docker/docker-compose.yml down -v
```

## Troubleshooting

1. **Container Issues**
   - If containers fail to start, check logs:
     ```bash
     docker-compose -f docker/docker-compose.yml logs
     ```

2. **Database Connection Issues**
   - Ensure PostgreSQL container is running:
     ```bash
     docker ps | grep postgres
     ```

3. **DAG Not Showing**
   - Check if the DAG file is in the correct location
   - Verify file permissions
   - Check Airflow logs for any import errors

## Contributing

Feel free to submit issues and enhancement requests!
