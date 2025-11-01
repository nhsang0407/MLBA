from project_retail.connectors.connector import Connector
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# ==============================
# HÀM: Phân loại khách hàng theo Tên phim
# ==============================
def classifyCustomersByFilm(conn):

    # Câu SQL: lấy danh sách phim và khách hàng đã thuê
    sql = """
        SELECT 
            f.film_id,
            f.title AS film_title,
            c.customer_id,
            CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
            COUNT(r.rental_id) AS total_rentals
        FROM film f
        JOIN inventory i ON f.film_id = i.film_id
        JOIN rental r ON i.inventory_id = r.inventory_id
        JOIN customer c ON r.customer_id = c.customer_id
        GROUP BY f.film_id, f.title, c.customer_id, c.first_name, c.last_name
        ORDER BY f.title, customer_name;
    """

    # Lấy dữ liệu vào DataFrame
    df = conn.queryDataset(sql)

    # In ra kiểm tra
    print(df.head(10))

    # Gom nhóm theo tên phim (groupby)
    grouped = df.groupby("film_title")["customer_name"].apply(list).reset_index()

    # Hiển thị kết quả
    for index, row in grouped.iterrows():
        print(f"\n🎬 {row['film_title']}")
        print("Khách hàng đã thuê:")
        for customer in row['customer_name']:
            print(f" - {customer}")

    # Trả về DataFrame để dùng tiếp (ví dụ hiển thị web, vẽ biểu đồ, ...)
    return grouped


def classifyCustomersByCategory(conn):
    # 2. Truy vấn SQL
    sql = """
        SELECT 
            cat.category_id,
            cat.name AS category_name,
            c.customer_id,
            CONCAT(c.first_name, ' ', c.last_name) AS customer_name
        FROM category cat
        JOIN film_category fc ON cat.category_id = fc.category_id
        JOIN film f ON fc.film_id = f.film_id
        JOIN inventory i ON f.film_id = i.film_id
        JOIN rental r ON i.inventory_id = r.inventory_id
        JOIN customer c ON r.customer_id = c.customer_id
        GROUP BY cat.category_id, cat.name, c.customer_id, c.first_name, c.last_name
        ORDER BY cat.name, c.last_name, c.first_name;
    """

    # 3. Lấy dữ liệu vào DataFrame
    df = conn.queryDataset(sql)

    # 4. Loại bỏ dữ liệu trùng lặp (nếu có)
    df = df.drop_duplicates(subset=["category_id", "customer_id"])

    # 5. Gom nhóm theo Category
    grouped = df.groupby("category_name")["customer_name"].apply(list).reset_index()

    # 6. Hiển thị kết quả
    for index, row in grouped.iterrows():
        print(f"\n📂 Category: {row['category_name']}")
        print("Khách hàng đã thuê:")
        for customer in row['customer_name']:
            print(f" - {customer}")

    # 7. Trả kết quả (dùng cho web hoặc phân tích tiếp)
    return grouped


def build_customer_features(conn, top_n_categories=5):
    """
    Trả về DataFrame features cho mỗi customer.
    - conn: Connector đã kết nối (instance)
    - top_n_categories: số category hàng đầu để tạo các cột đặc trưng
    """
    # 1) Aggregates cơ bản: tổng rentals, số film distinct, số inventory distinct, recency (days)
    sql_agg = """
    SELECT
        c.customer_id,
        COUNT(r.rental_id) AS total_rentals,
        COUNT(DISTINCT f.film_id) AS unique_films,
        COUNT(DISTINCT i.inventory_id) AS unique_inventory,
        DATEDIFF(CURDATE(), MAX(r.rental_date)) AS recency_days,
        MIN(r.rental_date) AS first_rental_date,
        MAX(r.rental_date) AS last_rental_date
    FROM customer c
    JOIN rental r ON c.customer_id = r.customer_id
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film f ON i.film_id = f.film_id
    GROUP BY c.customer_id
    ;
    """
    df_agg = conn.queryDataset(sql_agg)
    if df_agg is None or df_agg.empty:
        raise ValueError("Không có dữ liệu rental. Kiểm tra database/sakila.")

    # 2) Tính avg_rentals_per_month (nếu có khoảng thời gian)
    # convert dates if necessary (pandas may parse)
    df_agg['first_rental_date'] = pd.to_datetime(df_agg['first_rental_date'])
    df_agg['last_rental_date'] = pd.to_datetime(df_agg['last_rental_date'])
    # avoid zero division
    df_agg['active_months'] = ((df_agg['last_rental_date'] - df_agg['first_rental_date']).dt.days / 30.0).replace(0, np.nan)
    df_agg['avg_rentals_per_month'] = df_agg['total_rentals'] / df_agg['active_months']
    df_agg['avg_rentals_per_month'] = df_agg['avg_rentals_per_month'].fillna(df_agg['total_rentals'])  # fallback

    # drop helper cols after
    df_agg = df_agg.drop(columns=['first_rental_date','last_rental_date','active_months'])

    # 3) Tìm top N categories theo tổng lượt thuê (để giảm chiều dữ liệu)
    sql_top_categories = f"""
    SELECT cat.category_id, cat.name, COUNT(*) AS rent_count
    FROM category cat
    JOIN film_category fc ON cat.category_id = fc.category_id
    JOIN film f ON fc.film_id = f.film_id
    JOIN inventory i ON f.film_id = i.film_id
    JOIN rental r ON i.inventory_id = r.inventory_id
    GROUP BY cat.category_id, cat.name
    ORDER BY rent_count DESC
    LIMIT {top_n_categories};
    """
    top_cat_df = conn.queryDataset(sql_top_categories)
    top_categories = top_cat_df['name'].tolist() if (top_cat_df is not None and not top_cat_df.empty) else []

    # 4) Lấy số lần thuê theo customer x category (chỉ top categories)
    if top_categories:
        # Build IN list safe for SQL
        cats_escaped = ",".join(["'{}'".format(str(x).replace("'", "''")) for x in top_categories])
        sql_cat_by_customer = f"""
        SELECT
            c.customer_id,
            cat.name AS category_name,
            COUNT(*) AS cnt
        FROM customer c
        JOIN rental r ON c.customer_id = r.customer_id
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category cat ON fc.category_id = cat.category_id
        WHERE cat.name IN ({cats_escaped})
        GROUP BY c.customer_id, cat.name;
        """
        df_cat = conn.queryDataset(sql_cat_by_customer)
        if df_cat is None:
            df_cat = pd.DataFrame(columns=['customer_id','category_name','cnt'])
        # pivot
        pivot = df_cat.pivot_table(index='customer_id', columns='category_name', values='cnt', fill_value=0)
        # rename columns to safe names
        pivot.columns = [f"cat_{str(c).replace(' ','_')}_cnt" for c in pivot.columns]
        # join to df_agg
        df_features = df_agg.merge(pivot, how='left', left_on='customer_id', right_index=True)
    else:
        df_features = df_agg.copy()

    # fillna zeros for category cols
    cat_cols = [col for col in df_features.columns if col.startswith('cat_')]
    df_features[cat_cols] = df_features[cat_cols].fillna(0)

    # final feature set: choose numeric columns we want to use
    features = [
        'total_rentals',
        'unique_films',
        'unique_inventory',
        'recency_days',
        'avg_rentals_per_month'
    ] + cat_cols

    # ensure all features exist
    features = [f for f in features if f in df_features.columns]

    return df_features[['customer_id'] + features], features


def build_and_cluster_customers(conn=None, n_clusters=4, top_n_categories=5, random_state=42):
    """
    Full pipeline:
     - nếu conn là None: tạo Connector(database='sakila') bên trong
     - build features, scale, kmeans
     - return (df_result, model, scaler, features)
    """
    # 1) ensure connector
    created_conn = False
    if conn is None:
        conn = Connector(database="sakila")
        conn.connect()
        created_conn = True

    # 2) build features
    df_features, feature_cols = build_customer_features(conn, top_n_categories=top_n_categories)

    # 3) scale
    scaler = StandardScaler()
    X = df_features[feature_cols].values
    X_scaled = scaler.fit_transform(X)

    # 4) run KMeans
    model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10, max_iter=300)
    labels = model.fit_predict(X_scaled)

    # 5) attach labels
    df_result = df_features.copy()
    df_result['cluster'] = labels

    # 6) compute centroids in original feature space (inverse transform)
    centroids_scaled = model.cluster_centers_
    centroids_orig = scaler.inverse_transform(centroids_scaled)
    centroids_df = pd.DataFrame(centroids_orig, columns=feature_cols)
    centroids_df['cluster'] = range(len(centroids_df))

    # 7) silhouette score (optional, only if n_clusters>1)
    sil_score = None
    if len(set(labels)) > 1:
        try:
            sil_score = silhouette_score(X_scaled, labels)
        except Exception:
            sil_score = None

    # close connector if we opened it
    if created_conn:
        try:
            conn.close()
        except Exception:
            pass

    return {
        'df': df_result,
        'model': model,
        'scaler': scaler,
        'features': feature_cols,
        'centroids': centroids_df,
        'silhouette_score': sil_score
    }


# ==============================
# GỌI HÀM CHẠY THỬ
# ==============================
if __name__ == "__main__":
    # Kết nối đến cơ sở dữ liệu sakila
    conn = Connector(database="sakila")
    conn.connect()

    result = classifyCustomersByFilm(conn)
    print("\nTổng số phim:", len(result))

    result = classifyCustomersByCategory(conn)
    print("\nTổng số Category:", len(result))


    out = build_and_cluster_customers(conn=conn, n_clusters=4, top_n_categories=5)
    df_with_clusters = out['df']
    print("Features used:", out['features'])
    print("Silhouette score:", out['silhouette_score'])
    print(df_with_clusters.head())
    print("\nCentroids (original scale):")
    print(out['centroids'])
