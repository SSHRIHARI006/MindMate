import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from scipy.stats import chi2_contingency
from sklearn.feature_selection import f_classif
from imblearn.over_sampling import SMOTE
from imblearn.combine import SMOTEENN
from sklearn.model_selection import train_test_split

# Load dataset
path = "Model Training/Student Depression Dataset.csv"
df = pd.read_csv(path)

# Data exploration
df.info()
print(df.isnull().sum())

# Fill missing values in 'Financial Stress' with median
x = df['Financial Stress'].median()
df['Financial Stress'].fillna(x, inplace=True)

# Drop unnecessary column
df.drop(['id'], axis=1, inplace=True)

# Group-wise analysis
print(df.groupby('Depression')['Financial Stress'].mean())
print(df.groupby('Depression')['Age'].mean())
print(df.groupby('Gender')['Depression'].count())
print(df.groupby('Depression')['Academic Pressure'].mean())
print(df.groupby('Depression')['CGPA'].mean())
print(df.groupby('Depression')['Study Satisfaction'].mean())

# Data Visualization
df.hist(bins=30, edgecolor='black')
plt.title('Distribution of Features')
plt.show()

sns.scatterplot(x=df['CGPA'], y=df['Academic Pressure'])
plt.title('Scatter plot between CGPA and Academic Pressure')
plt.show()

# Filter data for students only
df = df[df['Profession'] == 'Student']
df.drop(['Profession', 'Work Pressure', 'Job Satisfaction'], axis=1, inplace=True)

# Encode categorical variables
label_encoder = LabelEncoder()
categorical_features = ['Gender', 'Degree', 'City', 'Dietary Habits', 
                        'Have you ever had suicidal thoughts ?', 'Sleep Duration', 
                        'Family History of Mental Illness']
for column in categorical_features:
    df[column] = label_encoder.fit_transform(df[column])

# Correlation Heatmap
correlation_matrix = df.corr()
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix Heatmap')
plt.show()

# Chi-Square Test for categorical features
for feature in categorical_features:
    contingency_table = pd.crosstab(df[feature], df['Depression'])
    chi2, p, _, _ = chi2_contingency(contingency_table)
    print(f"Feature: {feature} | Chi-Square: {chi2} | p-value: {p}\n")

# ANOVA F-test for numerical features
numerical_features = ['Sleep Duration', 'City', 'CGPA', 'Academic Pressure', 
                      'Work/Study Hours', 'Financial Stress']
f_scores, p_values = f_classif(df[numerical_features], df['Depression'])
anova_results = pd.DataFrame({'Feature': numerical_features, 'F-Score': f_scores, 'p-value': p_values})
print(anova_results)

# Standardization
scaler = StandardScaler()
df[numerical_features] = scaler.fit_transform(df[numerical_features])

# Normalization
scaler = MinMaxScaler()
df[numerical_features] = scaler.fit_transform(df[numerical_features])

# Selecting final features
df_final = df[['Sleep Duration', 'Academic Pressure', 'Dietary Habits', 
               'Work/Study Hours', 'Financial Stress', 'Have you ever had suicidal thoughts ?', 'Depression']]
df = df_final

# Correlation Heatmap after preprocessing
correlation_matrix = df.corr()
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix Heatmap (After Preprocessing)')
plt.show()

# Handling Imbalanced Data with SMOTE
X = df.drop('Depression', axis=1)
y = df['Depression']

# Apply SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Apply SMOTEENN
smote_enn = SMOTEENN(random_state=42)
X_resampled_enn, y_resampled_enn = smote_enn.fit_resample(X, y)

print("Data preprocessing completed! Ready to apply models.")
df.to_csv("Model Training/Student Depression Dataset.csv", index=False)
