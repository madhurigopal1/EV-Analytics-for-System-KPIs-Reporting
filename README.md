# EV Analytics for System — KPIs & Reporting

A production-oriented proof of concept for EV product and customer KPI reporting. Spring Boot provides the dashboard API and optional AWS Bedrock chatbot; Python generates and loads reproducible synthetic records and computes analytics; MySQL is the shared source of truth; AngularJS provides a small dashboard UX.

## Architecture

- `backend/`: Java 17 / Spring Boot REST API, JDBC KPI queries, AWS Bedrock Runtime chatbot integration, health endpoint.
- `python/`: FastAPI data/analytics service, SQLAlchemy + PyMySQL, deterministic synthetic dataset generator (10,000 customers, 10,000 products, 50,000 transactions).
- `database/`: MySQL 8 schema and indexes, mounted as first-start initialization SQL.
- `frontend/`: AngularJS single-page KPI dashboard and chat panel.
- `docker-compose.yml`: local integrated stack with health checks and persistent MySQL volume.

## Start the full stack

Requirements: Docker Compose v2.

```bash
cp .env.example .env
docker compose up --build
```

Open the dashboard at <http://localhost:8080>. Spring API is available at <http://localhost:8080/api/kpis> and Spring Actuator health at <http://localhost:8080/actuator/health>. Python service is at <http://localhost:8000/docs>.

The Python service loads the synthetic dataset on container startup only if the database is empty. To trigger a load explicitly:

```bash
curl -X POST http://localhost:8000/admin/generate
```

`POST /admin/generate` is a development/demo operation; protect or disable it before exposing this service outside a trusted network.

## AWS Bedrock chatbot (optional)

Set `AWS_REGION` and `BEDROCK_MODEL_ID` in `.env`, and provide credentials through the normal AWS SDK credential chain (for example, an IAM role or locally mounted shared credentials). Do not put access keys in source control. The selected model must be enabled for the AWS account/region. Without Bedrock configuration, the chatbot returns a clearly labeled local KPI-based fallback rather than failing the dashboard.

The bot receives aggregate KPI context only; it is not given individual customer records. Review AWS data handling, model availability, IAM permissions, and retention requirements before production use.

## Data and production considerations

All records are fictional, generated demo data—not actual customer data or forecasts. KPI definitions are in `backend/.../KpiService.java`; validate them with business owners before decisions. Before production, add authentication/authorization, secret management, migrations, audit trails, rate limiting, observability, backups, privacy controls, and a reviewed data governance policy. AngularJS 1.x is retained to match the requested stack; it is end-of-life and should be upgraded for a production product.

## Python analytics pipeline

`python/app/main.py` exposes readiness, dataset generation, and aggregate KPI endpoints. `python/app/analytics.py` computes segment/category summaries from the same MySQL data used by the Java API. The generator is deterministic for reproducibility and uses batched inserts to avoid loading all transactions as one SQL statement.

## Configuration

See `.env.example`. The compose defaults are for local development only. If running Spring or Python outside Docker, use a local MySQL instance and configure `SPRING_DATASOURCE_URL` / `DATABASE_URL` accordingly.

No test suite is included in this POC.
