# Medical Telegram Data Warehouse

## Project Overview

This project builds an end-to-end data platform for collecting, storing, transforming, and analyzing data from Ethiopian medical and pharmaceutical Telegram channels.

The solution follows a modern ELT architecture:

1. Extract Telegram messages and images using Telethon.
2. Store raw data in a structured data lake.
3. Load raw data into PostgreSQL.
4. Transform data into a dimensional star schema using dbt.
5. Apply data quality tests and documentation.
6. Enrich image data using YOLOv8 object detection.
7. Perform analytical reporting on message engagement and visual content.

---

## Project Objectives

* Collect data from public medical Telegram channels.
* Build a scalable data lake structure.
* Design a star schema for analytical reporting.
* Implement data quality testing with dbt.
* Detect objects in images using YOLOv8.
* Analyze relationships between visual content and engagement metrics.

---

## Technology Stack

### Data Collection

* Python
* Telethon
* Telegram API

### Data Storage

* PostgreSQL

### Data Transformation

* dbt (Data Build Tool)

### Computer Vision

* YOLOv8 (Ultralytics)

### Data Processing

* Pandas
* SQLAlchemy

### Development Tools

* VS Code
* Git
* GitHub

---

## Project Structure

medical-telegram-warehouse/
│
├── data/
│   ├── raw/
│   │   ├── telegram_messages/
│   │   └── images/
│   │
│   └── processed/
│
├── logs/
│
├── src/
│   ├── scrape_telegram.py
│   ├── load_raw_to_postgres.py
│   ├── yolo_detect.py
│   └── load_image_detections.py
│
├── medical_warehouse/
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   │
│   ├── tests/
│   ├── assert_positive_views.sql
│   └── assert_no_future_messages.sql
│
├── analysis/
│   └── image_analysis.sql
│
├── docs/
│
├── requirements.txt
├── README.md
└── .gitignore

---

## Data Sources

Telegram Channels:

* CheMed123
* lobelia4cosmetics
* tikvahpharma

Additional medical channels can be added by updating the channel list in the scraper configuration.

---

## Task 1: Data Extraction and Loading

### Features

* Extract Telegram messages
* Download images
* Store raw JSON files
* Create log files
* Load data into PostgreSQL

### Run Scraper

```bash
python src/scrape_telegram.py
```

### Load Data into PostgreSQL

```bash
python src/load_raw_to_postgres.py
```

---

## PostgreSQL Schema

### Raw Table

```sql
CREATE TABLE raw.telegram_messages (
    message_id BIGINT,
    channel_name VARCHAR(200),
    message_date TIMESTAMP,
    message_text TEXT,
    views INTEGER,
    forwards INTEGER,
    has_media BOOLEAN,
    image_path TEXT
);
```

---

## Task 2: Data Modeling with dbt

### Star Schema

#### Fact Table

* fct_messages

#### Dimension Tables

* dim_channels
* dim_dates

### Run dbt Models

```bash
dbt run
```

### Run Tests

```bash
dbt test
```

### Generate Documentation

```bash
dbt docs generate
```

### Serve Documentation

```bash
dbt docs serve
```

---

## Data Quality Tests

### Generic Tests

* unique
* not_null
* relationships

### Custom Tests

#### assert_no_future_messages.sql

Ensures no future-dated messages exist.

#### assert_positive_views.sql

Ensures view counts are non-negative.

---

## Task 3: Image Enrichment Using YOLOv8

### Install YOLO

```bash
pip install ultralytics
```

### Run Object Detection

```bash
python src/yolo_detect.py
```

### Output

```text
data/processed/image_detections.csv
```

### Image Categories

| Category        | Description                 |
| --------------- | --------------------------- |
| promotional     | Person and product detected |
| product_display | Product detected, no person |
| lifestyle       | Person detected, no product |
| other           | Neither detected            |

---

## Analytical Questions

The project investigates:

1. Do promotional posts receive more views than product-display posts?
2. Which channels publish the most visual content?
3. What are the limitations of using generic object detection models for medical products?

---

## Environment Variables

Create a `.env` file:

```env
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
```

### Obtain Telegram API Credentials

1. Visit https://my.telegram.org
2. Login using your Telegram account.
3. Open API Development Tools.
4. Create an application.
5. Copy the API ID and API Hash.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/medical-telegram-warehouse.git
cd medical-telegram-warehouse
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies


pip install -r requirements.txt


