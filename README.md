# Distributed Multi-Model Analytics for E-Commerce Data

**AUCA Big Data Analytics Final Project**  
**Student:** SHEMA Joshua Rwaka  
**Student ID:** 101342  
**Date:** June 2026  

## Project Overview
This project implements a multi-model analytics system for large-scale e-commerce data using MongoDB, HBase, and Apache Spark.

## Technologies Used
- **MongoDB** — Document store for products, users, and transactions
- **HBase** — Wide-column store for time-series session data (simulated)
- **Apache Spark (PySpark)** — Distributed batch processing and SQL analytics
- **Python** — Data generation, loading, and visualization

## Project Structure
| File | Description |
|------|-------------|
| `dataset_generator_clean.py` | Generates synthetic e-commerce dataset |
| `load_mongodb.py` | Loads data into MongoDB |
| `mongodb_queries.py` | MongoDB aggregation pipelines |
| `hbase_simulation.py` | HBase schema design and query simulation |
| `spark_analysis.py` | Spark batch processing and SQL analytics |
| `integrated_analytics.py` | CLV, product affinity, and cohort analysis |
| `visualizations.py` | Charts and visualizations |

## Dataset
- 10,000 users
- 5,000 products across 25 categories
- 500,000 transactions
- 2,000,000 browsing sessions (90 days)

## Key Findings
- Top customer spent $80,881 across 73 orders
- Credit card was the highest revenue payment method ($117M)
- Mobile users had the highest conversion rate at 21.6%
- Peak revenue day: June 4, 2026 at $5.43M
