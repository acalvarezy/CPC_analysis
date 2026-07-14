#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# 1. LOAD DATA
file_path = r"/Users/catalinaalvarez/Google Drive/My Drive/UVA/Research/JanesLab/CPC_project/CPC experimental/06-19-26 BUB1 inhibition/BUB1 inhibitions quantification.xlsx"
df = pd.read_excel(file_path)


# Get percentages
df["zero_p"] = df["zero"]/df["total"]
df["one_p"] = df["one"]/df["total"]
df["two_p"] = df["two"]/df["total"]
df["bilobed_p"] = df["bilobed"]/df["total"]

#Expand data to include patterns
data_long = pd.melt(
    df, 
    id_vars=['Image', 'treatment'],          # Columns to keep unchanged
    value_vars=['zero_p', 'one_p', 'two_p', 'bilobed_p'], # Columns to unpivot into rows
    var_name='pattern',           # Name for the new category column
    value_name='percentage'        # Name for the new values column
)

# Set a clean layout style
sns.set_theme(style="darkgrid")

# Create a grouped violin plot
plt.figure(figsize=(10, 6))

sns.violinplot(
    data=data_long, 
    x="treatment", 
    y="percentage", 
    hue="pattern", 
    palette="muted"
)


plt.title("Distribution of CPC recruitment patterns")
plt.savefig("/Users/catalinaalvarez/Google Drive/My Drive/UVA/Research/JanesLab/CPC_project/CPC experimental/06-19-26 BUB1 inhibition/BUB1_inh.pdf")

plt.show()


# %%
