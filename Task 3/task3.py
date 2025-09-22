import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder

# =========================
# 1. Load Dataset
# =========================
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "bank.csv")  

df = pd.read_csv(file_path, sep=';')
print("✅ Dataset Loaded Successfully!\n")
print(" First 5 Rows:")
print(df.head())
print("\n Dataset Info:")
print(df.info())
print("\n Missing Values per Column:")
print(df.isnull().sum())

# =========================
# 2. Data Cleaning & Encoding
# =========================
le = LabelEncoder()
for col in df.select_dtypes(include=['object']).columns:
    df[col] = le.fit_transform(df[col])

print("\n✅ Encoding Done! Here’s the cleaned data:")
print(df.head())

# =========================
# 3. Feature Selection
# =========================
X = df.drop('y', axis=1)
y = df['y']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("\n✅ Data Split Completed!")
print("Training Samples:", X_train.shape[0])
print("Testing Samples:", X_test.shape[0])

# =========================
# 4. Build Decision Tree Model
# =========================
clf = DecisionTreeClassifier(criterion="entropy", max_depth=3, random_state=42)
clf.fit(X_train, y_train)
print("\n✅ Decision Tree Model Trained Successfully!")

# =========================
# 5. Model Evaluation
# =========================
y_pred = clf.predict(X_test)
print("\n📈 Model Accuracy:", accuracy_score(y_test, y_pred))
print("\n📊 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\n📄 Classification Report:\n", classification_report(y_test, y_pred))

# =========================
# 6. Visualization
# =========================

# Decision Tree Plot
plt.figure(figsize=(20, 10))
plot_tree(
    clf,
    feature_names=X.columns,
    class_names=['No', 'Yes'],
    filled=True,
    rounded=True,
    fontsize=10
)
plt.title("Decision Tree Classifier")
plt.tight_layout()
plt.savefig("decision_tree.png")
plt.show()

# Confusion Matrix Plot
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=['No', 'Yes'], yticklabels=['No', 'Yes'])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.show()

# Feature Importance
plt.figure(figsize=(10, 5))
sns.barplot(x=clf.feature_importances_, y=X.columns)
plt.title("Feature Importance in Decision Tree")
plt.tight_layout()
plt.savefig("feature_importance.png")
plt.show()

print("\n✅ Visualizations Saved (decision_tree.png, confusion_matrix.png, feature_importance.png)")
