#Load the required packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Load the datasets
ds1 = pd.read_csv("train_dataset.csv")
print(ds1) 

clean_dataset = ds1.dropna()
print(clean_dataset)
