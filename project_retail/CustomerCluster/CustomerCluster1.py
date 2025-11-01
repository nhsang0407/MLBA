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

showHistogram(df,df.columns[1:])


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
elbowMethod(df,columns)

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

visualizeKMeans(X,
                y_kmeans,
                cluster,
                "Clusters of Customers - Age X Spending Score",
                "Age",
                "Spending Score",
                colors)
# k=5
columns=['Annual_Income','Spending_Score']
elbowMethod(df,columns)
X = df.loc[:, columns].values
cluster=5

y_kmeans,centroids,labels=runKMeans(X,cluster)
print(y_kmeans)
print(centroids)
print(labels)
df["cluster"]=labels
print(df)

visualizeKMeans(X,
                y_kmeans,
                cluster,
                "Clusters of Customers - Annual Income X Spending Score",
                "Annual Income",
                "Spending Score",
                colors)

# k=6
columns=['Age','Annual_Income','Spending_Score']
elbowMethod(df,columns)
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
visualize3DKmeans(df,columns,hover_data,cluster)
