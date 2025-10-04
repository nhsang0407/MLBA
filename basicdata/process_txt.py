import pandas as pd

df=pd.read_csv("../dataset/SalesTransactions/SalesTransactions.txt",
               sep="\t", encoding="utf-8")
print(df)