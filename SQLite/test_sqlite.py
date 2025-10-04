import sqlite3
import pandas as pd
try:
    #Connect to DB and create a cursor
    sqliteConnection=sqlite3.connect('../databases/Chinook_Sqlite.sqlite')
    cursor=sqliteConnection.cursor()
    print('DB Init')
    #Write a query and execute it with cursor
    query=' select * from InvoiceLine LIMIT 5;'
    cursor.execute(query)
    #Fetch and output result
    df=pd.DataFrame(cursor.fetchall())
    print(df)
    #Close the cursor
    cursor.close()
#Handle errors
except sqlite3.Error as error:
    print("Error occured:", error)
#Close DB connection  irrespective of success or failure
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print('Sqlite Connection closed')

def get_top_invoices_by_value(a, b, N):
    query = f"""
        SELECT InvoiceId, Total
        FROM Invoice
        WHERE Total BETWEEN {a} AND {b}
        ORDER BY Total DESC
        LIMIT {N};
    """
    with sqlite3.connect('../databases/Chinook_Sqlite.sqlite') as conn:
        df = pd.read_sql_query(query, conn)
    return df

def get_top_customers_by_invoice_count(N):
    query = f"""
        SELECT c.CustomerId, c.FirstName || ' ' || c.LastName AS CustomerName,
               COUNT(i.InvoiceId) AS InvoiceCount
        FROM Customer c
        JOIN Invoice i ON c.CustomerId = i.CustomerId
        GROUP BY c.CustomerId
        ORDER BY InvoiceCount DESC
        LIMIT {N};
    """
    with sqlite3.connect('../databases/Chinook_Sqlite.sqlite') as conn:
        df = pd.read_sql_query(query, conn)
    return df

def get_top_customers_by_invoice_value(N):
    query = f"""
        SELECT c.CustomerId, c.FirstName || ' ' || c.LastName AS CustomerName,
               SUM(i.Total) AS TotalValue
        FROM Customer c
        JOIN Invoice i ON c.CustomerId = i.CustomerId
        GROUP BY c.CustomerId
        ORDER BY TotalValue DESC
        LIMIT {N};
    """
    with sqlite3.connect('../databases/Chinook_Sqlite.sqlite') as conn:
        df = pd.read_sql_query(query, conn)
    return df

print(get_top_invoices_by_value(5, 20, 10))       # Top 10 Invoice có total từ 5 đến 20
print(get_top_customers_by_invoice_count(5))      # Top 5 khách hàng nhiều Invoice nhất
print(get_top_customers_by_invoice_value(5))      # Top 5 khách hàng có tổng Invoice lớn nhất
