# EV Analytics for System — KPIs & Reporting

A production-oriented proof of concept for EV customer and product KPI reporting, recommendation generation, and conversational business analysis. This stack integrates:

- Java Spring Boot for API services and KPI orchestration
- AngularJS for a lightweight user dashboard
- MySQL 8 for transactional and KPI data storage
- Python + FastAPI for synthetic data generation and analytic summaries
- AWS Bedrock-powered conversational KPI assistant
- Docker Compose for local orchestration

## Overview

This project is designed for an EV business reporting scenario where analysts and leadership need to understand:

- revenue and order trends
- customer segments and churn risk
- product performance by category
- inventory and pricing health
- roadmap from current-state reporting to future-state EV intelligence

It uses synthetic, deterministic data to demonstrate a realistic analytics story without exposing real customer or business data.

## Solution architecture

- `backend/`: Spring Boot application exposing KPI endpoints and a conversational AI assistant
- `python/`: FastAPI service for data generation and summary analytics
- `database/`: MySQL schema initialization scripts
- `frontend/`: AngularJS dashboard
- `docker-compose.yml`: local multi-service deployment
- `.env.example`: environment values for local development

## Repository structure

```text
EV-Analytics-for-System-KPIs-Reporting/
├── backend/
│   ├── Dockerfile
│   ├── pom.xml
│   └── src/
│       ├── main/
│       │   ├── java/com/evanalytics/
│       │   │   ├── EvAnalyticsApplication.java
│       │   │   ├── controller/
│       │   │   │   ├── KpiController.java
│       │   │   │   └── ChatController.java
│       │   │   ├── dto/
│       │   │   │   ├── KpiSummary.java
│       │   │   │   ├── SegmentKpi.java
│       │   │   │   ├── ProductKpi.java
│       │   │   └── service/
│       │   │       ├── KpiService.java
│       │   │       └── BedrockChatService.java
│       │   └── resources/
│       │       ├── application.properties
│       │       └── static/
│       │           └── index.html
├── python/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── analytics.py
│       ├── data_pipeline.py
│       └── main.py
├── database/
│   └── schema.sql
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
└── LICENSE
```

## Tech stack

- Java 17
- Spring Boot 3.3
- AngularJS 1.x
- MySQL 8
- Python 3.12
- FastAPI
- SQLAlchemy
- PyMySQL
- AWS Bedrock Runtime SDK

## Functional capabilities

### KPI reporting

The backend queries MySQL for:

- total customer count
- total product count
- completed orders
- revenue totals
- average order value
- average churn risk
- segment-level customer KPIs
- product-category KPIs

### Conversational analytics assistant

The AI bot answers questions such as:

- Which customer segment has the highest churn risk?
- Which product category is underperforming?
- Which market should receive more attention?
- What should be the next phase of our EV analytics roadmap?

The bot is connected to AWS Bedrock when configured. If AWS is not configured, it falls back to local KPI-inspired guidance so the dashboard remains operational.

### Roadmap and recommendations

The dashboard includes recommendation themes such as:

1. KPI governance and data quality
2. Automated ingestion and monitoring
3. Predictive churn and demand analysis
4. Business-user friendly conversational analytics
5. Future EV intelligence and strategic operations

## Data model

This project uses synthetic data with the following scale:

- 10,000 customer records
- 10,000 product records
- 50,000 sales transactions

### Customer table

```sql
customers (
    id BIGINT PRIMARY KEY,
    customer_name VARCHAR(120),
    segment VARCHAR(32),
    city VARCHAR(80),
    region VARCHAR(32),
    age SMALLINT,
    annual_income DECIMAL(12,2),
    purchase_frequency SMALLINT,
    tenure_months SMALLINT,
    churn_risk DECIMAL(5,4),
    created_at DATETIME
)
```

### Product table

```sql
products (
    id BIGINT PRIMARY KEY,
    product_name VARCHAR(120),
    category VARCHAR(40),
    model_type VARCHAR(32),
    battery_capacity_kwh DECIMAL(7,2),
    price DECIMAL(12,2),
    efficiency_score DECIMAL(5,2),
    stock_quantity INT,
    launch_date DATE
)
```

### Sales transaction table

```sql
sales_transactions (
    id BIGINT PRIMARY KEY,
    customer_id BIGINT,
    product_id BIGINT,
    transaction_date DATETIME,
    quantity SMALLINT,
    unit_price DECIMAL(12,2),
    total_amount DECIMAL(14,2),
    sales_channel VARCHAR(32),
    region VARCHAR(32),
    status VARCHAR(16)
)
```

## Getting started

### 1. Configure environment

Create the local environment file:

```bash
cp .env.example .env
```

Update `.env` for your local environment if needed.

### 2. Start the full stack

```bash
docker compose up --build
```

This starts:

- MySQL on `localhost:3306`
- Python analytics service on `localhost:8000`
- Spring Boot API on `localhost:8080`
- AngularJS dashboard at `http://localhost:8080`

### 3. Open the dashboard

Navigate to:

```text
http://localhost:8080
```

### 4. Trigger data generation explicitly (optional)

The Python service generates its dataset automatically if the database is empty. If you want to regenerate intentionally, use:

```bash
curl -X POST http://localhost:8000/admin/generate
```

This is intended for local demo use. Disable or secure it before exposing the service outside a trusted environment.

## API endpoints

### Spring Boot

```text
GET /api/kpis
GET /api/kpis/segments
GET /api/kpis/products
POST /api/chat
GET /actuator/health
```

### Python analytics service

```text
GET /health
GET /analytics/summary
GET /analytics/segments
GET /analytics/products
POST /admin/generate
```

## AWS Bedrock integration

The chatbot is implemented as an optional AWS Bedrock Runtime integration.

Required environment variables:

- `AWS_REGION`
- `BEDROCK_MODEL_ID`

You should provide AWS credentials via a standard AWS SDK credential source, such as:

- IAM role
- AWS profile
- workload identity
- secret manager or secure runtime injection

Do not store AWS access keys in source control.

Without a valid Bedrock configuration, the bot falls back to a local response instead of failing the app. This keeps the dashboard usable while preserving the AI-assisted design pattern.

## Roadmap: current state to future state

### Current state

- fragmented source data
- manual KPI reporting
- limited business-user self-service
- disconnected decision visibility

### Near-term future

- KPI governance model and metric ownership
- automated validation for customer and product feeds
- dashboard refreshes from a single trusted data store

### Mid-term future

- predictive analytics for churn, inventory, and demand
- category-level and segment-level forecasting
- role-based operational dashboards

### Target future state

- executive-grade EV intelligence layer
- AI-assisted analysis and recommendation engine
- fleet, charging, and service cross-domain analytics
- closed-loop operational decision making

## Recommended strategy

1. Standardize KPI definitions across business units.
2. Establish trusted data pipelines and ownership.
3. Add exception monitoring and anomaly detection.
4. Use AI-assisted analytics for business interpretation and recommendation generation.
5. Expand to EV battery, charging, service, and fleet lifecycle metrics after governance is stable.

## Production considerations

This application is intentionally designed as a local proof-of-concept, not a production system. Before production deployment, consider:

- authentication and authorization
- secrets management
- CI/CD and release pipelines
- DB migration versioning
- rate limiting and API security
- observability and logging
- backup and disaster recovery
- privacy and compliance review
- synthetic data removal before connecting real data
- model governance and prompt review if using AWS Bedrock

## Notes

- Data is intentionally synthetic and fictional.
- The dashboard and APIs are designed for demo-friendly KPI analysis.
- AngularJS is retained to match the requested stack; for a production system, a modern frontend framework should be considered.
- No automated test suite is included in this POC.

## License

This project is intended for demonstration and learning purposes.

## Summary

This repo demonstrates a realistic EV KPI analytics platform that blends business reporting, data operations, and conversational insights. It provides a conceptually complete architecture for a local POC and can be extended into a larger enterprise solution with governance, forecasting, and operational analytics.
