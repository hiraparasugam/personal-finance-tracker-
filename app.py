import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Personal Finance Tracker",
    page_icon="💰",
    layout="wide"
)

st.title("💰 AI Personal Finance Tracker")
st.markdown("""
### Features
- 📊 Spending Analytics
- 💡 AI Insights
- 📈 Expense Forecasting
- 💰 Financial Health Tracking
- 📥 Downloadable Reports
""")

# -----------------------------
# EXPENSE CATEGORIZATION
# -----------------------------
def categorize(description):

    desc = str(description).lower()

    # Family Support
    if "ramesh hirapara" in desc:
        return "Family Support"

    # Specific Friends
    elif "arya pravi" in desc:
        return "Friend Transfer"

    elif "master adi" in desc:
        return "Friend Transfer"

    # Bills
    elif any(x in desc for x in [
        "bil/",
        "electricity",
        "recharge",
        "bill"
    ]):
        return "Bills"

    # Bank Transfers
    elif any(x in desc for x in [
        "neft",
        "imps",
        "rtgs"
    ]):
        return "Bank Transfer"

    # ATM
    elif "atm" in desc:
        return "Cash Withdrawal"

    # Card Payments
    elif any(x in desc for x in [
        "pos",
        "debit card",
        "credit card"
    ]):
        return "Card Payment"

    # Remaining UPI
    elif "upi/" in desc:
        return "UPI Transfer"

    else:
        return "Other"

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload Bank Statement CSV",
    type=["csv"]
)

if uploaded_file:

    try:

        # -----------------------------
        # READ BANK STATEMENT
        # -----------------------------
        df = pd.read_csv(uploaded_file, skiprows=12)

        df.columns = [
            "Ignore",
            "SNo",
            "ValueDate",
            "TransactionDate",
            "ChequeNumber",
            "Description",
            "Withdrawal",
            "Deposit",
            "Balance"
        ]

        df = df.drop(columns=["Ignore"])

        # -----------------------------
        # CLEAN DATA
        # -----------------------------
        for col in ["Withdrawal", "Deposit", "Balance"]:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).fillna(0)

        # -----------------------------
        # CATEGORY
        # -----------------------------
        df["Category"] = df["Description"].apply(categorize)

        st.success("CSV loaded successfully")

        st.dataframe(
            df[
                [
                   "TransactionDate",
                   "Description",
                   "Category",
                   "Withdrawal",
                   "Deposit"
                ]
            ].head(20)
        )
        
        # -----------------------------
        #METRICS
        # -----------------------------
        
        total_income = df["Deposit"].sum()
        total_expense = df["Withdrawal"].sum()
        savings = total_income - total_expense
        transaction_count = len(df)
        
        largest_expense = df["Withdrawal"].max()

        avg_expense = (
            total_expense / transaction_count
            if transaction_count > 0
            else 0
        )

        col1, col2, col3 = st.columns(3)
        
        col1.metric(
            "💰 Income",
            f"₹{total_income:,.0f}"
        )

        col2.metric(
            "💸 Expense",
            f"₹{total_expense:,.0f}"
        )

        col3.metric(
            "🏦 Savings",
            f"₹{savings:,.0f}"
        )

        col4, col5, col6 = st.columns(3)

        col4.metric(
        "📄 Transactions",
        transaction_count
        )

        col5.metric(
        "🔥 Largest Expense",
        f"₹{largest_expense:,.0f}"
        )

        col6.metric(
        "📊 Avg Expense",
        f"₹{avg_expense:,.0f}"
        )

        # -----------------------------
        # SIDEBAR DASHBOARD
        # -----------------------------
        
        st.sidebar.title("💰 Finance Dashboard")

        st.sidebar.metric(
            "Income",
            f"₹{total_income:,.0f}"
        )

        st.sidebar.metric(
            "Expense",
            f"₹{total_expense:,.0f}"
        )

        st.sidebar.metric(
            "Savings",
            f"₹{savings:,.0f}"
        )

        st.sidebar.metric(
            "Transactions",
            transaction_count
        )
        
        # -----------------------------
        # CATEGORY ANALYSIS
        # -----------------------------
        
        category_summary = (
            df.groupby("Category")["Withdrawal"]
            .sum()
            .reset_index()
        )
        category_summary = category_summary[
            category_summary["Withdrawal"] > 0
        ]
        if len(category_summary) > 0:

            st.subheader("📊 Expense Distribution")
            
            fig_pie = px.pie(
                category_summary,
                names="Category",
                values="Withdrawal",
                hole=0.4
            )

            st.plotly_chart(
                fig_pie,
                use_container_width=True
            )
            
        # -----------------------------    
        # NEW BAR CHART
        # -----------------------------
        
        fig_bar = px.bar(
            category_summary.sort_values(
                by="Withdrawal",
                ascending=False
            ),
            x="Category",
            y="Withdrawal",
            title="Top Spending Categories"
        )
        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )
        st.subheader("💵 Spending by Category")
        
        st.dataframe(
            category_summary.sort_values(
                by="Withdrawal",
                ascending=False
            )
        )
        
        # DOWNLOAD REPORT
        
        csv_report = category_summary.to_csv(
                index=False)
        
        st.download_button(
            label="📥 Download Expense Report",
            data=csv_report,
            file_name="expense_report.csv",
            mime="text/csv"
        )

        # -----------------------------
        # AI INSIGHT
        # -----------------------------
        
        top_expenses = (
            df.sort_values(
                by="Withdrawal",
                ascending=False
            )
            .head(10)
        )
        highest = category_summary.loc[
            category_summary["Withdrawal"].idxmax()
        ]
        
        avg_monthly = avg_expense
     
        largest_txn = top_expenses.iloc[0]
        
        savings_rate = (
            (savings / total_income) * 100
            if total_income > 0
            else 0
        )
        
        st.subheader("🤖 AI Insights")
        
        st.info(
            f"""
            💡 Financial Summary
            
        • Total Transactions: {transaction_count}
        
        • Largest Expense:
        ₹{largest_txn['Withdrawal']:,.0f}
        
        • Average Monthly Expense:
        ₹{avg_monthly:,.0f} 
        
        • Highest Spending Category:
        {highest['Category']}
        
        • Savings Rate:
        {savings_rate:.1f}%
        """
        )
        
        # -----------------------------
        #Top 10 Expenses Table
        # -----------------------------
        
        st.subheader("🔥 Top 10 Expenses")

        st.dataframe(
            top_expenses[
                [
                    "TransactionDate",
                    "Description",
                    "Withdrawal"
                ]
            ]
        )
        
        # -----------------------------
        # MONTHLY TREND
        # -----------------------------
        
        try:
            
            df["TransactionDate"] = pd.to_datetime(
                df["TransactionDate"],
                errors="coerce"
            )
            
            monthly = (
                df.groupby(
                    df["TransactionDate"].dt.to_period("M")
                )["Withdrawal"]
                .sum()
                .reset_index()
            )   
            
            monthly["TransactionDate"] = (
                  monthly["TransactionDate"]
                .astype(str)
            )

            st.subheader("📈 Monthly Expense Trend")

            fig_line = px.line(
                monthly,            
                x="TransactionDate",
                y="Withdrawal",
                title="Monthly Expense Trend",
                markers=True
            )
            
            st.plotly_chart(
                fig_line,
                use_container_width=True
            )
            
            # -----------------------------
            # ML FORECAST
            # -----------------------------
            
            if len(monthly) >= 2:
                monthly["MonthNumber"] = np.arange(
                    len(monthly)
                )

                X = monthly[["MonthNumber"]]
                y = monthly["Withdrawal"]

                model = LinearRegression()
                model.fit(X, y)

                next_month = len(monthly)

                prediction = model.predict(
                    [[next_month]]
                )[0]

                st.subheader(
                    "🤖 Next Month Expense Forecast"
                )

                st.info(
                    f"Estimated next month's spending: ₹{prediction:,.2f}"
                )           
            
            else:
                st.info(
                    "Need at least 2 months of data for forecasting."
                )   
        except Exception as e:
            st.exception(e)
            
    except Exception as e:
        st.exception(e)