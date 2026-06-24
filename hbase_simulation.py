# HBase Schema Design and Query Simulation
# Since HBase requires Docker/cloud setup, we demonstrate
# the schema design and query logic using Python dictionaries
# that mirror exactly how HBase would store and retrieve data

import json
from datetime import datetime

print("=" * 60)
print("HBASE SCHEMA DESIGN")
print("=" * 60)

print("""
TABLE 1: user_sessions
  Row Key: user_id + reverse_timestamp (e.g. user_000042_9999999999)
  Column Families:
    session_info: session_id, start_time, end_time, duration_seconds
    device:       type, os, browser
    geo:          city, state, country, ip_address
    behavior:     conversion_status, referrer, viewed_products

  WHY THIS DESIGN:
  - Row key starts with user_id so all sessions for one user are stored together
  - Reverse timestamp means most recent sessions come first
  - Efficient for: "Get all sessions for user X in last 30 days"

TABLE 2: product_performance
  Row Key: product_id + date (e.g. prod_00123_2026-06-04)
  Column Families:
    metrics:  total_views, cart_additions, purchases, revenue
    inventory: stock_level, is_active

  WHY THIS DESIGN:
  - Row key combines product + date for time-series tracking
  - Efficient for: "Get product X performance over last 90 days"
""")

# Simulate loading session data
print("=" * 60)
print("LOADING SESSION DATA FOR HBASE SIMULATION")
print("=" * 60)

with open("sessions_0.json") as f:
    sessions = json.load(f)

# Simulate HBase table: user_sessions
print("\nSimulating HBase user_sessions table...")
hbase_user_sessions = {}

for session in sessions[:1000]:  # Use first 1000 sessions
    user_id = session["user_id"]
    start_time = session["start_time"]
    session_id = session["session_id"]
    
    # Create row key: user_id + timestamp
    row_key = f"{user_id}_{start_time}"
    
    hbase_user_sessions[row_key] = {
        "session_info:session_id": session_id,
        "session_info:start_time": start_time,
        "session_info:end_time": session["end_time"],
        "session_info:duration_seconds": session["duration_seconds"],
        "device:type": session["device_profile"]["type"],
        "device:os": session["device_profile"]["os"],
        "device:browser": session["device_profile"]["browser"],
        "geo:city": session["geo_data"]["city"],
        "geo:country": session["geo_data"]["country"],
        "behavior:conversion_status": session["conversion_status"],
        "behavior:referrer": session["referrer"]
    }

print(f"Stored {len(hbase_user_sessions)} rows in user_sessions table")

# Query 1: Get all sessions for a specific user
print("\n" + "=" * 60)
print("HBASE QUERY 1: Get all sessions for user_000042")
print("=" * 60)

target_user = "user_000042"
user_sessions = {k: v for k, v in hbase_user_sessions.items() 
                 if k.startswith(target_user)}

print(f"Found {len(user_sessions)} sessions for {target_user}")
for row_key, data in list(user_sessions.items())[:3]:
    print(f"\nRow Key: {row_key}")
    print(f"  Device: {data['device:type']} / {data['device:os']}")
    print(f"  Location: {data['geo:city']}, {data['geo:country']}")
    print(f"  Status: {data['behavior:conversion_status']}")
    print(f"  Referrer: {data['behavior:referrer']}")

# Query 2: Conversion rate by device type
print("\n" + "=" * 60)
print("HBASE QUERY 2: Conversion Rate by Device Type")
print("=" * 60)

device_stats = {}
for data in hbase_user_sessions.values():
    device = data["device:type"]
    status = data["behavior:conversion_status"]
    if device not in device_stats:
        device_stats[device] = {"converted": 0, "total": 0}
    device_stats[device]["total"] += 1
    if status == "converted":
        device_stats[device]["converted"] += 1

for device, stats in device_stats.items():
    rate = (stats["converted"] / stats["total"]) * 100
    print(f"{device}: {rate:.1f}% conversion ({stats['converted']}/{stats['total']})")

print("\nHBase simulation complete!")