import os
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import streamlit as st

# ──────────────────────────────────────────────────────────────────────────────
# Load environment variables (Alpha Vantage API key)
load_dotenv()
av_token = os.getenv("AV_API_KEY")

# ──────────────────────────────────────────────────────────────────────────────
# Streamlit page config
st.set_page_config(
    page_title="Financial Dashboard (Interactive)",
    layout="wide",
)

# ──────────────────────────────────────────────────────────────────────────────
# Sidebar: Stock‐symbol selector
st.sidebar.header("🔍 Select Stock Symbol")
symbol = st.sidebar.selectbox(
    "Choose a ticker:", 
    ["AAPL", "META", "GOOG"], 
    index=0
)

# ──────────────────────────────────────────────────────────────────────────────
# Main title & subtitle
st.title(f"📊 {symbol} Financial Dashboard (Interactive)")
st.markdown(
    """
    Explore **8 interactive visualizations** of the chosen company’s income statement data 
    (2005–present) using the Alpha Vantage API and Plotly for charts.
    """
)

# ──────────────────────────────────────────────────────────────────────────────
# Display chosen symbol
st.write(f"### Stock Symbol: {symbol}")

# ──────────────────────────────────────────────────────────────────────────────
# Fetch data from Alpha Vantage
url = (
    f"https://www.alphavantage.co/query?"
    f"function=INCOME_STATEMENT&symbol={symbol}&apikey={av_token}"
)
response = requests.get(url)
if response.status_code != 200:
    st.error(f"API request failed with status code {response.status_code}")
    st.stop()

payload = response.json()
if "annualReports" not in payload:
    st.error("API response does not contain 'annualReports'.")
    st.stop()

# ──────────────────────────────────────────────────────────────────────────────
# Build DataFrame & preprocess
income_df = pd.DataFrame(payload["annualReports"])
income_df["fiscalDateEnding"] = pd.to_datetime(income_df["fiscalDateEnding"])
income_df["fiscalYear"] = income_df["fiscalDateEnding"].dt.year

# Convert numeric columns to floats
cols_to_numeric = [
    "grossProfit",
    "totalRevenue",
    "costOfRevenue",
    "costofGoodsAndServicesSold",
    "operatingIncome",
    "sellingGeneralAndAdministrative",
    "researchAndDevelopment",
    "operatingExpenses",
    "investmentIncomeNet",
    "netInterestIncome",
    "interestIncome",
    "interestExpense",
    "nonInterestIncome",
    "otherNonOperatingIncome",
    "depreciation",
    "depreciationAndAmortization",
    "incomeBeforeTax",
    "incomeTaxExpense",
    "interestAndDebtExpense",
    "netIncomeFromContinuingOperations",
    "comprehensiveIncomeNetOfTax",
    "ebit",
    "ebitda",
    "netIncome",
]
for col in cols_to_numeric:
    income_df[col] = pd.to_numeric(income_df[col], errors="coerce")

# Sort by year ascending
income_df = income_df.sort_values("fiscalYear")

# Calculate profit margin (%) column
income_df["profit_margin_pct"] = (
    income_df["netIncome"] / income_df["totalRevenue"] * 100
)

# ──────────────────────────────────────────────────────────────────────────────
# Sidebar filters
st.sidebar.header("🔍 Filters")

year_min = int(income_df["fiscalYear"].min())
year_max = int(income_df["fiscalYear"].max())
year_range = st.sidebar.slider(
    "Select Fiscal Year Range",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max),
)

# Filtered DF based on year range
df_filtered = income_df[
    (income_df["fiscalYear"] >= year_range[0])
    & (income_df["fiscalYear"] <= year_range[1])
].copy()

# Expense categories for multiselect
expense_options = [
    "sellingGeneralAndAdministrative",
    "researchAndDevelopment",
    "interestExpense",
]
selected_expenses = st.sidebar.multiselect(
    "Select Expense Categories (for Expense Breakdown)",
    options=expense_options,
    default=expense_options,
)

# Show a sample of filtered DataFrame
st.subheader("📄 Filtered Income Statement (Sample Columns)")
st.dataframe(
    df_filtered[
        ["fiscalYear", "totalRevenue", "netIncome", "grossProfit", "profit_margin_pct"]
    ].set_index("fiscalYear"),
    use_container_width=True,
)

# ──────────────────────────────────────────────────────────────────────────────
# Helper: Format y-axis as billions of USD
def bill_formatter(x):
    return f"${x/1e9:.0f}B"

# Helper: For numeric axes that should not be in billions
def plain_formatter(x):
    return f"{x:.1f}"

# ──────────────────────────────────────────────────────────────────────────────
# Row 1: Charts 1 & 2
row1_col1, row1_col2 = st.columns(2, gap="large")

# 1. Total Revenue Over Time (Bar Chart)
with row1_col1:
    st.subheader("1. 💵 Total Revenue Over Time")
    fig1 = px.bar(
        df_filtered,
        x="fiscalYear",
        y="totalRevenue",
        labels={"fiscalYear": "Year", "totalRevenue": "Total Revenue"},
        title="Total Revenue by Fiscal Year",
        hover_data={"totalRevenue": ":,.0f", "netIncome": ":,.0f"},
        color_discrete_sequence=["#1f77b4"],
    )
    fig1.update_yaxes(title_text="Revenue (Billion USD)", tickformat=",.0f")
    fig1.update_traces(hovertemplate="Year: %{x}<br>Revenue: %{y:$,.0f}")
    fig1.update_layout(
        xaxis=dict(tickmode="linear"),
        yaxis=dict(tickformat=".0f"),
        plot_bgcolor="white",
        font=dict(family="Arial", size=12),
    )
    st.plotly_chart(fig1, use_container_width=True)

# 2. Net Income Over Time (Line Chart)
with row1_col2:
    st.subheader("2. 📈 Net Income Over Time")
    fig2 = px.line(
        df_filtered,
        x="fiscalYear",
        y="netIncome",
        markers=True,
        labels={"fiscalYear": "Year", "netIncome": "Net Income"},
        title="Net Income by Fiscal Year",
        hover_data={"netIncome": ":,.0f", "totalRevenue": ":,.0f"},
        color_discrete_sequence=["green"],
    )
    fig2.update_yaxes(title_text="Net Income (Billion USD)", tickformat=",.0f")
    fig2.update_traces(hovertemplate="Year: %{x}<br>Net Income: %{y:$,.0f}")
    fig2.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="white",
        font=dict(family="Arial", size=12),
    )
    st.plotly_chart(fig2, use_container_width=True)

# ──────────────────────────────────────────────────────────────────────────────
# Row 2: Charts 3 & 4
row2_col1, row2_col2 = st.columns(2, gap="large")

# 3. Gross Profit vs Operating Income (Multi‐Line)
with row2_col1:
    st.subheader("3. 💰 Gross Profit vs Operating Income")
    fig3 = go.Figure()
    fig3.add_trace(
        go.Scatter(
            x=df_filtered["fiscalYear"],
            y=df_filtered["grossProfit"],
            mode="lines+markers",
            name="Gross Profit",
            marker=dict(symbol="circle", size=8),
            line=dict(color="#9467bd", width=2),
            hovertemplate="Year: %{x}<br>Gross Profit: %{y:$,.0f}<extra></extra>",
        )
    )
    fig3.add_trace(
        go.Scatter(
            x=df_filtered["fiscalYear"],
            y=df_filtered["operatingIncome"],
            mode="lines+markers",
            name="Operating Income",
            marker=dict(symbol="circle", size=8),
            line=dict(color="#d62728", width=2),
            hovertemplate="Year: %{x}<br>Operating Income: %{y:$,.0f}<extra></extra>",
        )
    )
    fig3.update_layout(
        title="Gross Profit vs Operating Income",
        xaxis=dict(title="Year", tickmode="linear"),
        yaxis=dict(title="Amount (Billion USD)", tickformat=",.0f"),
        plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="Arial", size=12),
    )
    st.plotly_chart(fig3, use_container_width=True)

# 4. EBITDA vs Net Income (Grouped Bar)
with row2_col2:
    st.subheader("4. 📊 EBITDA vs Net Income")
    fig4 = go.Figure()
    fig4.add_trace(
        go.Bar(
            x=[y - 0.2 for y in df_filtered["fiscalYear"]],
            y=df_filtered["ebitda"],
            width=0.4,
            name="EBITDA",
            marker_color="#ff7f0e",
            hovertemplate="Year: %{x}<br>EBITDA: %{y:$,.0f}<extra></extra>",
        )
    )
    fig4.add_trace(
        go.Bar(
            x=[y + 0.2 for y in df_filtered["fiscalYear"]],
            y=df_filtered["netIncome"],
            width=0.4,
            name="Net Income",
            marker_color="#2ca02c",
            hovertemplate="Year: %{x}<br>Net Income: %{y:$,.0f}<extra></extra>",
        )
    )
    fig4.update_layout(
        title="EBITDA vs Net Income",
        xaxis=dict(
            title="Year",
            tickmode="array",
            tickvals=df_filtered["fiscalYear"],
            ticktext=df_filtered["fiscalYear"],
        ),
        yaxis=dict(title="Amount (Billion USD)", tickformat=",.0f"),
        barmode="group",
        plot_bgcolor="white",
        font=dict(family="Arial", size=12),
    )
    st.plotly_chart(fig4, use_container_width=True)

# ──────────────────────────────────────────────────────────────────────────────
# Row 3: Charts 5 & 6
row3_col1, row3_col2 = st.columns(2, gap="large")

# 5. Expense Breakdown (Stacked Bar)
with row3_col1:
    st.subheader("5. 💸 Expense Breakdown (Stacked)")
    if selected_expenses:
        fig5 = go.Figure()
        for exp in selected_expenses:
            fig5.add_trace(
                go.Bar(
                    x=df_filtered["fiscalYear"],
                    y=df_filtered[exp],
                    name=exp.replace("sellingGeneralAndAdministrative", "SG&A")
                    .replace("researchAndDevelopment", "R&D")
                    .replace("interestExpense", "Interest Exp"),
                    hovertemplate="Year: %{x}<br>" + exp + ": %{y:$,.0f}<extra></extra>",
                )
            )
        fig5.update_layout(
            title="Major Expense Categories (Stacked)",
            xaxis=dict(title="Year", tickmode="linear"),
            yaxis=dict(title="Amount (Billion USD)", tickformat=",.0f"),
            barmode="stack",
            plot_bgcolor="white",
            font=dict(family="Arial", size=12),
        )
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.info("Select at least one expense category in the sidebar to display this chart.")

# 6. Revenue vs Cost of Revenue (Area Chart)
with row3_col2:
    st.subheader("6. 🔄 Revenue vs Cost of Revenue (Area)")
    fig6 = go.Figure()
    fig6.add_trace(
        go.Scatter(
            x=df_filtered["fiscalYear"],
            y=df_filtered["totalRevenue"],
            fill="tozeroy",
            name="Total Revenue",
            mode="none",
            fillcolor="rgba(31,119,180,0.5)",
            hovertemplate="Year: %{x}<br>Revenue: %{y:$,.0f}<extra></extra>",
        )
    )
    fig6.add_trace(
        go.Scatter(
            x=df_filtered["fiscalYear"],
            y=df_filtered["costOfRevenue"],
            fill="tozeroy",
            name="Cost of Revenue",
            mode="none",
            fillcolor="rgba(214,39,40,0.5)",
            hovertemplate="Year: %{x}<br>Cost: %{y:$,.0f}<extra></extra>",
        )
    )
    fig6.update_layout(
        title="Revenue vs Cost of Revenue",
        xaxis=dict(title="Year", tickmode="linear"),
        yaxis=dict(title="Amount (Billion USD)", tickformat=",.0f"),
        plot_bgcolor="white",
        font=dict(family="Arial", size=12),
    )
    st.plotly_chart(fig6, use_container_width=True)

# ──────────────────────────────────────────────────────────────────────────────
# Row 4: Charts 7 & 8
row4_col1, row4_col2 = st.columns(2, gap="large")

# 7. R&D vs SG&A Expenses (Line Chart)
with row4_col1:
    st.subheader("7. 🧪 R&D vs SG&A Expenses")
    fig7 = go.Figure()
    fig7.add_trace(
        go.Scatter(
            x=df_filtered["fiscalYear"],
            y=df_filtered["researchAndDevelopment"],
            mode="lines+markers",
            name="R&D",
            line=dict(color="#17becf", width=2),
            marker=dict(size=8),
            hovertemplate="Year: %{x}<br>R&D: %{y:$,.0f}<extra></extra>",
        )
    )
    fig7.add_trace(
        go.Scatter(
            x=df_filtered["fiscalYear"],
            y=df_filtered["sellingGeneralAndAdministrative"],
            mode="lines+markers",
            name="SG&A",
            line=dict(color="#9467bd", width=2),
            marker=dict(size=8),
            hovertemplate="Year: %{x}<br>SG&A: %{y:$,.0f}<extra></extra>",
        )
    )
    fig7.update_layout(
        title="R&D vs SG&A Expenses",
        xaxis=dict(title="Year", tickmode="linear"),
        yaxis=dict(title="Amount (Billion USD)", tickformat=",.0f"),
        plot_bgcolor="white",
        font=dict(family="Arial", size=12),
    )
    st.plotly_chart(fig7, use_container_width=True)

# 8. Profit Margin (%) Over Time (Line Chart)
with row4_col2:
    st.subheader("8. 📐 Profit Margin (%) Over Time")
    fig8 = px.line(
        df_filtered,
        x="fiscalYear",
        y="profit_margin_pct",
        markers=True,
        labels={"fiscalYear": "Year", "profit_margin_pct": "Profit Margin (%)"},
        title="Net Profit Margin (%) by Year",
        hover_data={"profit_margin_pct": ":.2f"},
        color_discrete_sequence=["#2ca02c"],
    )
    fig8.update_layout(
        xaxis=dict(tickmode="linear"),
        yaxis=dict(title="Profit Margin (%)"),
        plot_bgcolor="white",
        font=dict(family="Arial", size=12),
    )
    fig8.update_traces(hovertemplate="Year: %{x}<br>Margin: %{y:.2f}%<extra></extra>")
    st.plotly_chart(fig8, use_container_width=True)

# Footer with copyright (centered)
st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 14px;'>"
    "© All rights reserved @Richard Quansah 2025"
    "</div>",
    unsafe_allow_html=True,
)
