from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count, avg, explode, desc

# Start Spark
spark = SparkSession.builder \
    .appName("EcommerceAnalytics") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
print("Spark started!")

# Load data
print("Loading transactions...")
transactions = spark.read.json("transactions.json")

print("Loading users...")
users = spark.read.json("users.json")

print("Loading products...")
products = spark.read.json("products.json")

# Analysis 1: Total revenue per day
print("\n=== DAILY REVENUE (Top 10 Days) ===")
transactions.createOrReplaceTempView("transactions")
daily_revenue = spark.sql("""
    SELECT 
        SUBSTRING(timestamp, 1, 10) as date,
        ROUND(SUM(total), 2) as daily_revenue,
        COUNT(*) as num_transactions
    FROM transactions
    GROUP BY SUBSTRING(timestamp, 1, 10)
    ORDER BY daily_revenue DESC
    LIMIT 10
""")
daily_revenue.show()

# Analysis 2: Revenue by payment method
print("\n=== REVENUE BY PAYMENT METHOD ===")
payment_revenue = spark.sql("""
    SELECT 
        payment_method,
        ROUND(SUM(total), 2) as total_revenue,
        COUNT(*) as num_transactions,
        ROUND(AVG(total), 2) as avg_order_value
    FROM transactions
    GROUP BY payment_method
    ORDER BY total_revenue DESC
""")
payment_revenue.show()

# Analysis 3: Product recommendations (users who bought X also bought Y)
print("\n=== DATA CLEANING: Checking for nulls ===")
print(f"Transactions with null total: {transactions.filter(col('total').isNull()).count()}")
print(f"Transactions with null user_id: {transactions.filter(col('user_id').isNull()).count()}")

print("\nSpark analysis complete!")
spark.stop()