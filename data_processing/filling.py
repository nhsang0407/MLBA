from numpy import nan as NA
import pandas as pd

data=pd.DataFrame([[1., 6.5, 3.],
                     [3., NA, NA],
                     [NA, NA, NA],
                     [NA, 6.5, 4.]])
print(data)
print("-"*10)
cleaned=data.fillna(data.mean())
print(cleaned)