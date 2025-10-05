class MyStatistic:
    def find_orders_within_range(self, df, minValue, maxValue):
        #Tong gia tri tung don hang
        order_totals=df.groupby('OrderID').apply(lambda x: (x['UnitPrice']*x['Quantity']*(1-x['Discount'])).sum())
        # Lọc đơn hàng trong khoảng minValue - maxValue
        orders_within_range = order_totals[(order_totals >= minValue) & (order_totals <= maxValue)]
        # danh sách các mã đơn hàng không trùng nhau
        unique_orders = df[df['OrderID'].isin(orders_within_range.index)]['OrderID'].drop_duplicates().tolist()

        return unique_orders
