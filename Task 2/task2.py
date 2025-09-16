#Task2 - Data Cleaning & EDA on Titanic Dataset(.arff file)
import os
import arff
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#Load Dataset
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "phpMYEkMl.arff")

with open(file_path) as f:
    dataset = arff.load(f)

df = pd.DataFrame(dataset['data'], columns=[attr[0] for attr in dataset['attributes']])

print(" Dataset Loaded Successfully!")
print("\n First 5 Rows:")
print(df.head())
print("\n Dataset Info:")
print(df.info())
print("\n Missing Values per Column:")
print(df.isnull().sum())
print("\n Summary Statistics:")
print(df.describe(include='all'))

# Data Cleaning
print("\n Cleaning Data...")

# Convert numeric columns properly
numeric_cols = ['age', 'fare']
for col in numeric_cols:
    if col in df.columns:
        df[col] = df[col].astype(float)

# Fill missing numeric values with median
for col in numeric_cols:
    if col in df.columns and df[col].isnull().sum() > 0:
        df[col].fillna(df[col].median(), inplace=True)

# Fill missing categorical columns with mode
for col in df.select_dtypes(include=['object']).columns:
    if df[col].isnull().sum() > 0:
        df[col].fillna(df[col].mode()[0], inplace=True)

print("\nMissing Values Cleaned!")
print(df.isnull().sum())

# Save cleaned dataset
df.to_csv("cleaned_titanic.csv", index=False)
print("Cleaned dataset saved as 'cleaned_titanic.csv'")

# Exploratory Data Analysis (EDA)
# Survival Count
plt.figure(figsize=(6, 4))
sns.countplot(x='survived', data=df, palette='Set2')
plt.title("Survival Count")
plt.xlabel("Survived (0 = No, 1 = Yes)")
plt.ylabel("Count")
plt.savefig("eda_survival_count.png")
plt.close()

# Survival by Gender
plt.figure(figsize=(6, 4))
sns.countplot(x='sex', hue='survived', data=df, palette='Set1')
plt.title("Survival by Gender")
plt.savefig("eda_survival_by_gender.png")
plt.close()

# Age Distribution
plt.figure(figsize=(8, 4))
sns.histplot(df['age'], kde=True, bins=30)
plt.title("Age Distribution")
plt.savefig("eda_age_distribution.png")
plt.close()

# Class-wise Survival
plt.figure(figsize=(6, 4))
sns.countplot(x='pclass', hue='survived', data=df, palette='Set3')
plt.title("Survival by Passenger Class")
plt.savefig("eda_survival_by_class.png")
plt.close()

#Correlation Heatmap
plt.figure(figsize=(8, 6))
numeric_df = df.select_dtypes(include=[np.number])
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Heatmap")
plt.savefig("eda_correlation_heatmap.png")
plt.close()

print("\n EDA Completed! Charts saved in the same folder.")
