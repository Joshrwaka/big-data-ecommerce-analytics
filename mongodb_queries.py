from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce"]

# Query 1: Top 10 Best-Selling Products
print("=" * 50)
print("TOP 10 BEST-SELLING PRODUCTS")
print("=" * 50)

pipeline1 = [
    {"$unwind": "$items"},
    {"$group": {
        "_id": "$items.product_id",
        "total_quantity_sold": {"$sum": "$items.quantity"},
        "total_revenue": {"$sum": "$items.subtotal"}
    }},
    {"$sort": {"total_quantity_sold": -1}},
    {"$limit": 10}
]

results1 = list(db.transactions.aggregate(pipeline1))
for r in results1:
    print(f"Product: {r['_id']} | Qty Sold: {r['total_quantity_sold']} | Revenue: ${r['total_revenue']:.2f}")

# Query 2: Total Revenue by Payment Method
print("\n" + "=" * 50)
print("REVENUE BY PAYMENT METHOD")
print("=" * 50)

pipeline2 = [
    {"$group": {
        "_id": "$payment_method",
        "total_revenue": {"$sum": "$total"},
        "num_transactions": {"$sum": 1}
    }},
    {"$sort": {"total_revenue": -1}}
]

results2 = list(db.transactions.aggregate(pipeline2))
for r in results2:
    print(f"Payment: {r['_id']} | Revenue: ${r['total_revenue']:.2f} | Transactions: {r['num_transactions']}")

# Query 3: User Activity Summary
print("\n" + "=" * 50)
print("TOP 10 MOST ACTIVE USERS")
print("=" * 50)

pipeline3 = [
    {"$group": {
        "_id": "$user_id",
        "total_spent": {"$sum": "$total"},
        "num_orders": {"$sum": 1}
    }},
    {"$sort": {"total_spent": -1}},
    {"$limit": 10}
]

results3 = list(db.transactions.aggregate(pipeline3))
for r in results3:
    print(f"User: {r['_id']} | Total Spent: ${r['total_spent']:.2f} | Orders: {r['num_orders']}")

client.close()
print("\nDone!")