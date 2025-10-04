import pandas as pd

def find_orders_within_range(df, minValue, maxValue, sortType=True):
    # Tính tổng giá trị từng đơn hàng
    order_totals = df.groupby('OrderID').apply(
        lambda x: (x['UnitPrice'] * x['Quantity'] * (1 - x['Discount'])).sum()
    )

    # Lọc đơn hàng trong khoảng minValue - maxValue
    orders_within_range = order_totals[(order_totals >= minValue) & (order_totals <= maxValue)]

    # Sắp xếp theo sortType
    orders_sorted = orders_within_range.sort_values(ascending=sortType)

    # Chuyển thành DataFrame (OrderID, Sum)
    result_df = orders_sorted.reset_index()
    result_df.columns = ['OrderID', 'Sum']

    return result_df


# ==============================
df = pd.read_csv('../dataset/SalesTransactions/SalesTransactions.csv')

minValue = float(input("Nhập giá trị min: "))
maxValue = float(input("Nhập giá trị max: "))
sortType = input("Sắp xếp tăng dần? (y/n): ").strip().lower() == 'y'

result = find_orders_within_range(df, minValue, maxValue, sortType)
print(result)
