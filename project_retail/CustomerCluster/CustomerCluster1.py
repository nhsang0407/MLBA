from project_retail.connectors.connector import Connector

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
import numpy as np

conn=Connector(database="salesdatabase")
conn.connect()
sql = (
    'SELECT DISTINCT customer.CustomerId, Age, Annual_Income, Spending_Score '
    'FROM customer, customer_spend_score '
    'WHERE customer.CustomerId = customer_spend_score.CustomerId'
)
df=conn.queryDataset(sql)

# print(df)
print(df.head())
# print(df.describe())

def showHistogram(df,columns):
    plt.figure(1, figsize=(7,8))
    n=0
    for column in columns:
        n+=1
        plt.subplot(3,1,n)
        plt.subplots_adjust(hspace=0.5,wspace=0.5)
        sns.distplot(df[column],bins=32)
        plt.title(f'Histogram of {column}')
    plt.show()

#showHistogram(df,df.columns[1:])


def elbowMethod(df,columnsForElbow):
    X = df.loc[:, columnsForElbow].values
    inertia = []
    for n in range(1 , 11):
        model = KMeans(n_clusters = n,
                   init='k-means++',
                   max_iter=500,
                   random_state=42)
        model.fit(X)
        inertia.append(model.inertia_)

    plt.figure(1 , figsize = (15 ,6))
    plt.plot(np.arange(1 , 11) , inertia , 'o')
    plt.plot(np.arange(1 , 11) , inertia , '-' , alpha = 0.5)
    plt.xlabel('Number of Clusters') , plt.ylabel('Cluster sum of squared distances')
    plt.show()

columns=['Age','Spending_Score']
#elbowMethod(df,columns)

def runKMeans(X,cluster):
    model = KMeans(n_clusters=cluster,
                   init='k-means++',
                   max_iter=500,
                   random_state=42)
    model.fit(X)
    labels = model.labels_
    centroids = model.cluster_centers_
    y_kmeans = model.fit_predict(X)
    return y_kmeans,centroids,labels

# k=4
X = df.loc[:, columns].values
cluster=4
colors=["red","green","blue","purple","black","pink","orange"]

y_kmeans,centroids,labels=runKMeans(X,cluster)
print("y_kmeans:")
print(y_kmeans)
print("centroids:")
print(centroids)
print("labels:")
print(labels)
df["cluster"]=labels
print("df:")
print(df)

def visualizeKMeans(X,y_kmeans,cluster,title,xlabel,ylabel,colors):
    plt.figure(figsize=(10, 10))
    for i in range(cluster):
        plt.scatter(X[y_kmeans == i, 0],
                    X[y_kmeans == i, 1],
                    s=100,
                    c=colors[i],
                    label='Cluster %i'%(i+1))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

'''visualizeKMeans(X,
                y_kmeans,
                cluster,
                "Clusters of Customers - Age X Spending Score",
                "Age",
                "Spending Score",
                colors)'''
# k=5
columns=['Annual_Income','Spending_Score']
#elbowMethod(df,columns)
X = df.loc[:, columns].values
cluster=5

y_kmeans,centroids,labels=runKMeans(X,cluster)
print(y_kmeans)
print(centroids)
print(labels)
df["cluster"]=labels
print(df)

'''visualizeKMeans(X,
                y_kmeans,
                cluster,
                "Clusters of Customers - Annual Income X Spending Score",
                "Annual Income",
                "Spending Score",
                colors)'''

# k=6
columns=['Age','Annual_Income','Spending_Score']
#elbowMethod(df,columns)
X = df.loc[:, columns].values
cluster=6

y_kmeans,centroids,labels=runKMeans(X,cluster)
print(y_kmeans)
print(centroids)
print(labels)
df["cluster"]=labels
print(df)

def visualize3DKmeans(df,columns,hover_data,cluster):
    fig=px.scatter_3d(df,
                      x=columns[0],
                      y=columns[1],
                      z=columns[2],
                      color='cluster',
                      hover_data=hover_data,
                      category_orders={"cluster":range(0,cluster)},
                      )
    fig.update_layout(margin=dict(l=0,r=0,b=0,t=0))
    fig.show()
hover_data=df.columns
#visualize3DKmeans(df,columns,hover_data,cluster)

'''def showCustomersByCluster(df):
    clusters = sorted(df["cluster"].unique())
    for cluster in clusters:
        print(f"\n=== CLUSTER {cluster} ===")
        cluster_df = df[df["cluster"] == cluster]
        print(cluster_df.to_string(index=False))
        print(f"Total customers in Cluster {cluster}: {len(cluster_df)}")
showCustomersByCluster(df)'''

def showCustomersByCluster(df):
    clusters = sorted(df["cluster"].unique())
    cluster_data = {}

    for cluster in clusters:
        cluster_df = df[df["cluster"] == cluster]
        cluster_data[cluster] = {
            "data": cluster_df,
            "count": len(cluster_df)
        }
    return cluster_data


result = showCustomersByCluster(df)

for cluster, info in result.items():
    print(f"\n=== CLUSTER {cluster} ===")
    print(info["data"].to_string(index=False))
    print(f"Total customers in Cluster {cluster}: {info['count']}")




from flask import Flask, render_template_string, send_file
import pandas as pd
import io

app = Flask(__name__)

def showCustomersByClusterWeb(df):
    cluster_data = showCustomersByCluster(df)
    clusters = list(cluster_data.keys())

    cluster_tables = {
        c: cluster_data[c]["data"].to_html(index=False, classes="data-table")
        for c in clusters
    }
    cluster_counts = {
        c: cluster_data[c]["count"] for c in clusters
    }

    html_template = """
    <html>
    <head>
        <title>Customer Clusters Dashboard</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background: #f0f2f5;
                margin: 0;
                padding: 30px;
            }
            h1 {
                color: #007bff;
                text-align: center;
                margin-bottom: 20px;
            }
            .container {
                max-width: 1100px;
                background: white;
                margin: auto;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            label {
                font-weight: bold;
                color: #333;
            }
            select {
                padding: 8px 12px;
                margin-left: 10px;
                font-size: 16px;
                border-radius: 6px;
                border: 1px solid #ccc;
            }
            button {
                background-color: #007bff;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                transition: 0.3s;
            }
            button:hover {
                background-color: #0056b3;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                border-radius: 8px;
                overflow: hidden;
            }
            th, td {
                padding: 10px;
                text-align: center;
                border-bottom: 1px solid #e0e0e0;
            }
            th {
                background-color: #007bff;
                color: white;
                text-transform: uppercase;
            }
            tr:hover {
                background-color: #eaf4ff;
                transition: 0.2s;
            }
            .cluster-card {
                margin-top: 30px;
                padding: 20px;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                background: #fafafa;
                box-shadow: 0 3px 6px rgba(0,0,0,0.05);
            }
            .cluster-card h2 {
                color: #007bff;
                margin-bottom: 10px;
            }
            .total {
                font-weight: bold;
                color: #333;
                margin-top: 10px;
            }
        </style>
        <script>
            function showCluster() {
                const selected = document.getElementById('clusterSelect').value;
                const clusters = document.getElementsByClassName('cluster-table');
                for (let i = 0; i < clusters.length; i++) {
                    clusters[i].style.display = 'none';
                }
                document.getElementById('cluster-' + selected).style.display = 'block';
            }
        </script>
    </head>
    <body>
        <div class="container">
            <h1>Customer Clusters Dashboard</h1>
            <label for="clusterSelect">Select Cluster:</label>
            <select id="clusterSelect" onchange="showCluster()">
                {% for cluster in clusters %}
                    <option value="{{ cluster }}">{{ cluster }}</option>
                {% endfor %}
            </select>

            {% for cluster, table in cluster_tables.items() %}
                <div id="cluster-{{ cluster }}" class="cluster-table cluster-card" style="display: none;">
                    <h2>Cluster {{ cluster }}</h2>
                    {{ table|safe }}
                    <p class="total">Total customers: {{ cluster_counts[cluster] }}</p>
                    <form action="/download/{{ cluster }}" method="get">
                        <button type="submit">⬇ Download Cluster {{ cluster }} CSV</button>
                    </form>
                </div>
            {% endfor %}
        </div>

        <script>
            // Hiển thị cluster đầu tiên mặc định
            document.getElementById('cluster-{{ clusters[0] }}').style.display = 'block';
        </script>
    </body>
    </html>
    """

    @app.route('/')
    def index():
        return render_template_string(
            html_template,
            clusters=clusters,
            cluster_tables=cluster_tables,
            cluster_counts=cluster_counts
        )

    @app.route('/download/<int:cluster>')
    def download_cluster(cluster):
        cluster_df = df[df["cluster"] == cluster]
        csv_buffer = io.StringIO()
        cluster_df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        return send_file(
            io.BytesIO(csv_buffer.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'cluster_{cluster}.csv'
        )

    app.run(debug=True)


showCustomersByClusterWeb(df)

