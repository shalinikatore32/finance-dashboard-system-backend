from app.db.mongodb import get_transactions_collection

async def get_dashboard_summary():
    transactions_collection = get_transactions_collection()
    
    # Match stage to ignore deleted transactions
    match_stage = {"$match": {"is_deleted": False}}
    
    # Total income & expenses pipeline
    totals_pipeline = [
        match_stage,
        {"$group": {
            "_id": "$type",
            "totalAmount": {"$sum": "$amount"}
        }}
    ]
    
    totals_cursor = transactions_collection.aggregate(totals_pipeline)
    total_income = 0.0
    total_expense = 0.0
    
    async for doc in totals_cursor:
        if doc["_id"] == "income":
            total_income = doc["totalAmount"]
        elif doc["_id"] == "expense":
            total_expense = doc["totalAmount"]
            
    net_balance = total_income - total_expense
    
    # Category-wise totals pipeline
    category_pipeline = [
        match_stage,
        {"$group": {
            "_id": "$category",
            "totalAmount": {"$sum": "$amount"}
        }},
        {"$sort": {"totalAmount": -1}}
    ]
    
    category_cursor = transactions_collection.aggregate(category_pipeline)
    category_totals = []
    async for doc in category_cursor:
        category_totals.append({"category": doc["_id"], "total": doc["totalAmount"]})
        
    # Monthly trends
    monthly_pipeline = [
        match_stage,
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$date"},
                    "month": {"$month": "$date"},
                    "type": "$type"
                },
                "totalAmount": {"$sum": "$amount"}
            }
        },
        {"$sort": {"_id.year": 1, "_id.month": 1}}
    ]
    
    monthly_cursor = transactions_collection.aggregate(monthly_pipeline)
    monthly_trends = []
    async for doc in monthly_cursor:
        month_str = f"{doc['_id']['year']}-{str(doc['_id']['month']).zfill(2)}"
        monthly_trends.append({
            "month": month_str,
            "type": doc["_id"]["type"],
            "total": doc["totalAmount"]
        })
        
    # Recent transactions
    cursor = transactions_collection.find({"is_deleted": False}).sort("date", -1).limit(5)
    recent_transactions = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        doc.pop("_id")
        recent_transactions.append(doc)

    return {
        "summary": {
            "total_income": total_income,
            "total_expense": total_expense,
            "net_balance": net_balance
        },
        "category_totals": category_totals,
        "monthly_trends": monthly_trends,
        "recent_transactions": recent_transactions
    }
