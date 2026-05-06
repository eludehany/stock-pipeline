import random
import time
import json
from datetime import datetime

stocks = {
    "COMI": 65.50,
    "ETEL": 28.30,
    "HRHO": 15.20,
    "SWDY": 42.10,
}

def simulate_stock_change(symbol, current_price):
    change_percent = random.uniform(-2.0, 2.0)
    change_amount = round(current_price * change_percent / 100, 2)
    new_price = round(current_price + change_amount, 2)
    
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symbol": symbol,
        "price": new_price,
        "change": change_amount,
        "change_percent": round(change_percent, 2),
        "volume": random.randint(1000, 50000)
    }
    return data, new_price

print("📈 البورصة شغالة...")
print("-" * 50)

while True:
    for symbol, price in stocks.items():
        reading, new_price = simulate_stock_change(symbol, price)
        stocks[symbol] = new_price
        
        arrow = "🔴" if reading["change"] < 0 else "🟢"
        print(f"{arrow} {symbol}: {reading['price']} جنيه | "
              f"التغيير: {reading['change']} ({reading['change_percent']}%)")
        
        with open("stock_log.json", "a") as f:
            f.write(json.dumps(reading, ensure_ascii=False) + "\n")
    
    print("-" * 50)
    time.sleep(5)