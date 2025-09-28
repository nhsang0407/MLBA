from numpy import nan as NA
import pandas as pd

data=pd.DataFrame([[1., 6.5, 3.],
                     [1., NA, NA],
                     [NA, NA, NA],
                     [NA, 6.5, 3.]])
print(data)
print("-"*10)
#delete nhung dong co chua NA
cleaned=data.dropna()
print(cleaned)
print("-"*10)
#delete dong chi toan NA
cleaned2=data.dropna(how='all')
print(cleaned2)