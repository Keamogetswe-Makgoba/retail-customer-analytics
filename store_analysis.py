import pandas as pd
import matplotlib.pyplot as plt


try:
    df = pd.read_csv('OnlineRetail.csv', encoding='ISO-8859-1')
    print("✅ Retail data loaded successfully!")

    
    
    df = df.dropna(subset=['CustomerID'])
    
    
    df = df[df['Quantity'] > 0]

    
    df['TotalSales'] = df['Quantity'] * df['UnitPrice']

    print(f"\n--- Dataset Overview ---")
    print(f"Total Rows: {len(df)}")
    print(f"Unique Customers: {df['CustomerID'].nunique()}")
    print(f"Total Revenue: R{df['TotalSales'].sum():.2f}")

except FileNotFoundError:
    print("❌ Error: 'OnlineRetail.csv' not found in this folder.")


top_products = df.groupby('Description')['TotalSales'].sum().sort_values(ascending=False).head(10)

print("\n--- Top 10 Products by Revenue ---")
print(top_products)


plt.figure(figsize=(10, 6))
top_products.plot(kind='bar', color='skyblue')
plt.title('Top 10 Revenue-Generating Products')
plt.ylabel('Revenue (ZAR)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top_products.png')
print("\n✅ Chart saved as 'top_products.png'!")


customer_data = df.groupby('CustomerID').agg({
    'InvoiceNo': 'count',    # Frequency (Number of purchases)
    'TotalSales': 'sum'      # Monetary (Total spend)
}).rename(columns={'InvoiceNo': 'Frequency', 'TotalSales': 'Monetary'})

print("\n--- Top 5 'Whale' Customers (Highest Spenders) ---")
print(customer_data.sort_values('Monetary', ascending=False).head())


plt.figure(figsize=(10, 6))
plt.scatter(customer_data['Frequency'], customer_data['Monetary'], alpha=0.5, color='purple')
plt.title('Customer Behavior: Frequency vs. Monetary')
plt.xlabel('Number of Purchases (Frequency)')
plt.ylabel('Total Spend (Monetary - ZAR)')
plt.grid(True)
plt.savefig('customer_behavior.png')
print("\n✅ Scatter plot saved as 'customer_behavior.png'!")


df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])


df['Hour'] = df['InvoiceDate'].dt.hour

hourly_sales = df.groupby('Hour')['InvoiceNo'].nunique()


plt.figure(figsize=(10, 6))
hourly_sales.plot(kind='bar', color='gold')
plt.title('Peak Shopping Hours')
plt.xlabel('Hour of Day (24-hour format)')
plt.ylabel('Number of Transactions')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('peak_hours.png')
print("\n✅ Hourly trend saved as 'peak_hours.png'!")


best_hour = hourly_sales.idxmax()
print(f"The most popular time to shop is {best_hour}:00.")