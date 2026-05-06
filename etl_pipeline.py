import json
import sqlite3
from datetime import datetime

def extract():
    """بتجيب الداتا من ملف الـ JSON"""
    data = []
    with open("stock_log.json", "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))
    print(f"✅ Extract: جبنا {len(data)} صف")
    return data

def transform(data):
    """بتنظف وتحلل الداتا"""
    cleaned = []
    for row in data:
        # بتشيل أي صف فيه سعر سالب
        if row["price"] <= 0:
            continue
        
        # بتضيف عمود alert لو السعر اتغير أكتر من 1.5%
        row["alert"] = "🚨 تغيير كبير!" if abs(row["change_percent"]) > 1.5 else "normal"
        cleaned.append(row)
    
    print(f"✅ Transform: بعد التنظيف عندنا {len(cleaned)} صف")
    return cleaned

def load(data):
    """بتحط الداتا في قاعدة بيانات SQLite"""
    conn = sqlite3.connect("stock_warehouse.db")
    cursor = conn.cursor()
    
    # بيعمل الجدول لو مش موجود
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            symbol TEXT,
            price REAL,
            change REAL,
            change_percent REAL,
            volume INTEGER,
            alert TEXT
        )
    ''')
    
    # بيحط الداتا في الجدول
    for row in data:
        cursor.execute('''
            INSERT INTO stocks 
            (timestamp, symbol, price, change, change_percent, volume, alert)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            row["timestamp"],
            row["symbol"],
            row["price"],
            row["change"],
            row["change_percent"],
            row["volume"],
            row["alert"]
        ))
    
    conn.commit()
    conn.close()
    print(f"✅ Load: اتحفظت {len(data)} صف في قاعدة البيانات")

def show_summary():
    """بتعرض ملخص الداتا"""
    conn = sqlite3.connect("stock_warehouse.db")
    cursor = conn.cursor()
    
    print("\n📊 ملخص البورصة:")
    print("-" * 50)
    
    cursor.execute('''
        SELECT symbol, 
               MAX(price) as أعلى_سعر,
               MIN(price) as أقل_سعر,
               AVG(price) as متوسط_السعر,
               COUNT(*) as عدد_الصفقات
        FROM stocks 
        GROUP BY symbol
    ''')
    
    for row in cursor.fetchall():
        print(f"📈 {row[0]}: أعلى={row[1]} | أقل={row[2]} | متوسط={round(row[3],2)} | صفقات={row[4]}")
    
    print("\n🚨 التغييرات الكبيرة:")
    cursor.execute('''
        SELECT timestamp, symbol, price, change_percent 
        FROM stocks 
        WHERE alert != 'normal'
        ORDER BY timestamp DESC
        LIMIT 5
    ''')
    
    for row in cursor.fetchall():
        print(f"⚠️ {row[0]} | {row[1]} | السعر: {row[2]} | التغيير: {row[3]}%")
    
    conn.close()

# تشغيل الـ ETL
print("🔄 بدء ETL Pipeline...")
print("-" * 50)
data = extract()
cleaned_data = transform(data)
load(cleaned_data)
show_summary()
print("-" * 50)
print("✅ ETL خلص بنجاح!")