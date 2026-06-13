import kagglehub
import pandas as pd
import os
import matplotlib.pyplot as plt

# Download dataset
path = kagglehub.dataset_download(
    "uom220338n/personal-finance-dataset"
)

# Load CSV
file = os.path.join(path, "Personal_Finance_Dataset.csv")
df = pd.read_csv(file)

# Income, Expense, Savings
income = df[df["Type"] == "Income"]["Amount"].sum()
expense = df[df["Type"] == "Expense"]["Amount"].sum()

print("Total Income:", income)
print("Total Expense:", expense)
print("Savings:", income - expense)

# Category-wise expenses
category_expense = (
    df[df["Type"] == "Expense"]
    .groupby("Category")["Amount"]
    .sum()
)

print(category_expense)

# BAR CHART
category_expense.plot(kind="bar")

plt.title("Expenses by Category")
plt.xlabel("Category")
plt.ylabel("Amount")

plt.tight_layout()
plt.savefig("expense_chart.png")
plt.show()

# PIE CHART
plt.figure()

category_expense.plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.title("Expense Distribution")
plt.ylabel("")

plt.savefig("expense_pie_chart.png")
plt.show()

# Convert Date column to date format
df["Date"] = pd.to_datetime(df["Date"])

# Extract month
df["Month"] = df["Date"].dt.to_period("M")

# Monthly expenses
monthly_expense = (
    df[df["Type"] == "Expense"]
    .groupby("Month")["Amount"]
    .sum()
)

plt.figure(figsize=(10, 5))

monthly_expense.plot(kind="line", marker="o")

plt.title("Monthly Expense Trend")
plt.xlabel("Month")
plt.ylabel("Expense Amount")

plt.tight_layout()
plt.savefig("monthly_expense_trend.png")
plt.show()

# Income vs Expense Summary

summary = pd.DataFrame({
    "Type": ["Income", "Expense", "Savings"],
    "Amount": [income, expense, income - expense]
})

print("\nIncome vs Expense Summary")
print(summary)

plt.figure(figsize=(6, 4))

plt.bar(
    summary["Type"],
    summary["Amount"]
)

plt.title("Income vs Expense vs Savings")
plt.ylabel("Amount")

plt.tight_layout()
plt.savefig("income_expense_summary.png")
plt.show()

# Export expense data to CSV
category_expense.to_csv("expense_summary.csv")

#create app.py for streamlit
import streamlit as st
import pandas as pd

st.title("Personal Finance Tracker")

df = pd.read_csv("expense_summary.csv")

st.write(df)