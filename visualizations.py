import json
from pymongo import MongoClient
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce"]

print("Creating visualizations...")

# ---- CHART 1: Revenue by Payment Method ----
pipeline1 = [
    {"$group": {
        "_id": "$payment_method",
        "total_revenue": {"$sum": "$total"}
    }},
    {"$sort": {"total_revenue": -1}}
]
data1 = list(db.transactions.aggregate(pipeline1))
labels1 = [d["_id"] for d in data1]
values1 = [d["total_revenue"] / 1_000_000 for d in data1]

plt.figure(figsize=(10, 6))
bars = plt.bar(labels1, values1, color=["#2ecc71","#3498db","#e74c3c","#f39c12","#9b59b6","#1abc9c"])
plt.title("Total Revenue by Payment Method", fontsize=16, fontweight="bold")
plt.xlabel("Payment Method")
plt.ylabel("Revenue ($ Millions)")
for bar, val in zip(bars, values1):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f"${val:.1f}M", ha="center", fontsize=10)
plt.tight_layout()
plt.savefig("chart1_revenue_by_payment.png", dpi=150)
plt.close()
print("Chart 1 saved!")

# ---- CHART 2: Top 10 Best-Selling Products ----
pipeline2 = [
    {"$unwind": "$items"},
    {"$group": {
        "_id": "$items.product_id",
        "total_qty": {"$sum": "$items.quantity"}
    }},
    {"$sort": {"total_qty": -1}},
    {"$limit": 10}
]
data2 = list(db.transactions.aggregate(pipeline2))
products2 = [d["_id"] for d in data2]
qty2 = [d["total_qty"] for d in data2]

plt.figure(figsize=(12, 6))
bars = plt.barh(products2[::-1], qty2[::-1], color="#3498db")
plt.title("Top 10 Best-Selling Products (by Quantity)", fontsize=16, fontweight="bold")
plt.xlabel("Total Quantity Sold")
for bar, val in zip(bars, qty2[::-1]):
    plt.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
             str(val), va="center", fontsize=10)
plt.tight_layout()
plt.savefig("chart2_top_products.png", dpi=150)
plt.close()
print("Chart 2 saved!")

# ---- CHART 3: Conversion Rate by Device Type ----
device_data = {"mobile": {"converted": 72, "total": 333},
               "tablet": {"converted": 65, "total": 334},
               "desktop": {"converted": 61, "total": 333}}

devices = list(device_data.keys())
rates = [device_data[d]["converted"] / device_data[d]["total"] * 100 for d in devices]
colors = ["#e74c3c", "#f39c12", "#2ecc71"]

plt.figure(figsize=(8, 6))
bars = plt.bar(devices, rates, color=colors)
plt.title("Conversion Rate by Device Type", fontsize=16, fontweight="bold")
plt.xlabel("Device Type")
plt.ylabel("Conversion Rate (%)")
plt.ylim(0, 30)
for bar, val in zip(bars, rates):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f"{val:.1f}%", ha="center", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig("chart3_conversion_by_device.png", dpi=150)
plt.close()
print("Chart 3 saved!")

# ---- CHART 4: Daily Revenue Trend ----
pipeline4 = [
    {"$group": {
        "_id": {"$substr": ["$timestamp", 0, 10]},
        "daily_revenue": {"$sum": "$total"}
    }},
    {"$sort": {"_id": 1}}
]
data4 = list(db.transactions.aggregate(pipeline4))
dates4 = [d["_id"] for d in data4]
revenue4 = [d["daily_revenue"] / 1_000_000 for d in data4]

plt.figure(figsize=(14, 6))
plt.plot(dates4, revenue4, color="#2ecc71", linewidth=2)
plt.fill_between(range(len(dates4)), revenue4, alpha=0.3, color="#2ecc71")
plt.title("Daily Revenue Trend (90 Days)", fontsize=16, fontweight="bold")
plt.xlabel("Date")
plt.ylabel("Revenue ($ Millions)")
plt.xticks(range(0, len(dates4), 10),
           [dates4[i] for i in range(0, len(dates4), 10)],
           rotation=45)
plt.tight_layout()
plt.savefig("chart4_daily_revenue_trend.png", dpi=150)
plt.close()
print("Chart 4 saved!")

client.close()
print("\nAll 4 charts saved in your project folder!")