from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count, avg, datediff, to_date, max, min, round

spark = SparkSession.builder \
    .appName("IntegratedAnalytics") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
print("Spark started!")

# Load data
print("Loading data...")
transactions = spark.read.json("transactions.json")
users = spark.read.json("users.json")

# Register as SQL tables
transactions.createOrReplaceTempView("transactions")
users.createOrReplaceTempView("users")

# ============================================
# BUSINESS QUESTION 1: Customer Lifetime Value
# Which users generate the most value over time?
# ============================================
print("\n" + "=" * 60)
print("CUSTOMER LIFETIME VALUE (CLV) ESTIMATION")
print("=" * 60)

clv = spark.sql("""
    SELECT 
        t.user_id,
        COUNT(*) as total_orders,
        ROUND(SUM(t.total), 2) as total_spent,
        ROUND(AVG(t.total), 2) as avg_order_value,
        MIN(SUBSTRING(t.timestamp, 1, 10)) as first_purchase,
        MAX(SUBSTRING(t.timestamp, 1, 10)) as last_purchase,
        ROUND(SUM(t.total) / COUNT(*), 2) as clv_score
    FROM transactions t
    GROUP BY t.user_id
    ORDER BY total_spent DESC
    LIMIT 15
""")

print("Top 15 Customers by Lifetime Value:")
clv.show(15, truncate=False)

# ============================================
# BUSINESS QUESTION 2: Product Affinity
# Which products are frequently bought together?
# ============================================
print("\n" + "=" * 60)
print("PRODUCT AFFINITY ANALYSIS")
print("Which products are bought together most often?")
print("=" * 60)

product_affinity = spark.sql("""
    SELECT 
        t1.product_id as product_A,
        t2.product_id as product_B,
        COUNT(*) as times_bought_together
    FROM (
        SELECT transaction_id, items[0].product_id as product_id 
        FROM transactions
        WHERE SIZE(items) > 1
    ) t1
    JOIN (
        SELECT transaction_id, items[1].product_id as product_id 
        FROM transactions
        WHERE SIZE(items) > 1
    ) t2
    ON t1.transaction_id = t2.transaction_id
    WHERE t1.product_id != t2.product_id
    GROUP BY t1.product_id, t2.product_id
    ORDER BY times_bought_together DESC
    LIMIT 10
""")

print("Top 10 Product Pairs Bought Together:")
product_affinity.show(10, truncate=False)

# ============================================
# BUSINESS QUESTION 3: Cohort Analysis
# How do users registered in different months spend?
# ============================================
print("\n" + "=" * 60)
print("COHORT ANALYSIS: Spending by Registration Month")
print("=" * 60)

cohort = spark.sql("""
    SELECT 
        SUBSTRING(u.registration_date, 1, 7) as registration_month,
        COUNT(DISTINCT t.user_id) as active_users,
        ROUND(SUM(t.total), 2) as total_revenue,
        ROUND(AVG(t.total), 2) as avg_order_value,
        COUNT(*) as total_orders
    FROM transactions t
    JOIN users u ON t.user_id = u.user_id
    GROUP BY SUBSTRING(u.registration_date, 1, 7)
    ORDER BY registration_month
""")

print("Revenue by User Registration Month:")
cohort.show(truncate=False)

print("\nIntegrated analytics complete!")
spark.stop()