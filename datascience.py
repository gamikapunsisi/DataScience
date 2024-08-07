# -*- coding: utf-8 -*-
"""Untitled6.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15_3h2JL3r3nLAaNtEhJb4VB__f4EbikZ
"""

import pandas as pd

file_path = '/content/dataset_5_24_CW.csv'
df = pd.read_csv(file_path)

df.head()

statistics = df.describe()
statistics

#type 01 remove records
import numpy as np
seed = 232099
np.random.seed(seed)

df = df.sample(frac=1).reset_index(drop=True)
df = df.drop(df.sample(n=5, random_state=seed).index).reset_index(drop=True)

df.head()

#type 2 remove 5 records
import numpy as np

index_numbers = [
    "YR3COBSCCOMP232P-001",
    "YR3COBSCCOMP232P-002",
    "YR3COBSCCOMP232P-003",
    "YR3COBSCCOMP232P-004",
    "YR3COBSCCOMP232P-005",
    "YR3COBSCCOMP232P-006",
    "YR3COBSCCOMP232P-007",
    "YR3COBSCCOMP232P-008",
    "YR3COBSCCOMP232P-009",
    "YR3COBSCCOMP232P-010"
]

np.random.seed(232099)

remove_indices = np.random.choice(len(index_numbers), size=5, replace=False)


print("Indices to remove:", remove_indices)

index_numbers_remaining = [index_numbers[i] for i in range(len(index_numbers)) if i not in remove_indices]

print("Remaining index numbers:")
for index_number in index_numbers_remaining:
    batch_number = index_number.split('-')[0][-4:]
    print(f"Batch Number: {batch_number}, Index Number: {index_number}")

incorrect_age = df[df['Age'] <= 0]
incorrect_work_exp = df[df['WorkExp (Years)']< 0]
incorrect_income = df[(df['MonthlyIncome (Rs)'] <= 0) | (df['HouseholdIncome (Rs)'] <= 0)]

incorrect_values = pd.concat([incorrect_age, incorrect_work_exp, incorrect_income]).drop_duplicates()

df_cleaned = df.drop(incorrect_values.index).reset_index(drop=True)

df_cleaned.head()

numeric_columns = df_cleaned.select_dtypes(include=[np.number]).columns

df_cleaned[numeric_columns] = df_cleaned[numeric_columns].apply(lambda x: x.fillna(x.median()))



df_cleaned.isna().sum()
df_cleaned.head()

df_cleaned['WorkExp_Binned'] = pd.cut(df_cleaned['WorkExp (Years)'], bins=4, labels=False)

print(df_cleaned.head())



from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

df_cleaned[['Age', 'MonthlyIncome (Rs)']] = scaler.fit_transform(df_cleaned[['Age', 'MonthlyIncome (Rs)']])
print(df_cleaned.head())



import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
sns.histplot(df_filled['Age'], bins=10, kde=True)
plt.title('Distribution of Age')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(x=df_cleaned['WorkExp (Years)'], y=df_cleaned['MonthlyIncome (Rs)'])
plt.title('Monthly Income vs. Work Experience')
plt.xlabel('Work Experience (Years)')
plt.ylabel('Monthly Income (Rs)')
plt.show()

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print(os.listdir('/content/'))

df_cleaned = pd.read_csv('/content/dataset_5_24_CW.csv')

# Min-max normalization function
def min_max_normalize(column):
    return (column - column.min()) / (column.max() - column.min())

df_cleaned['Age_normalized'] = min_max_normalize(df_cleaned['Age'])
df_cleaned['MonthlyIncome_normalized'] = min_max_normalize(df_cleaned['MonthlyIncome (Rs)']) # Changed column name here

print(df_cleaned)

# normalized Age
plt.figure(figsize=(10, 6))
sns.histplot(df_cleaned['Age_normalized'], bins=10, kde=True)
plt.title('Distribution of Normalized Age')
plt.xlabel('Normalized Age')
plt.ylabel('Count')
plt.show()

# normalized MonthlyIncome
plt.figure(figsize=(10, 6))
sns.histplot(df_cleaned['MonthlyIncome_normalized'], bins=10, kde=True)
plt.title('Distribution of Normalized Monthly Income')
plt.xlabel('Normalized Monthly Income')
plt.ylabel('Count')
plt.show()

colors = np.random.choice(['blue', 'green'], size=len(df_cleaned))

# normalized Age vs. normalized MonthlyIncome scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(df_cleaned['Age_normalized'], df_cleaned['MonthlyIncome_normalized'], alpha=0.5, c=colors)
plt.title('Normalized Age vs. Normalized Monthly Income')
plt.xlabel('Normalized Age')
plt.ylabel('Normalized Monthly Income')
plt.show()