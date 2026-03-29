import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

st.set_page_config(page_title="PhonePe Dashboard", layout="wide")

st.title("📊 PhonePe Transaction Insights")

# Upload files
uploaded_files = st.file_uploader(
    "Upload JSON Files", accept_multiple_files=True
)

data_list = []

if uploaded_files:
    for i, file in enumerate(uploaded_files):
        data = json.load(file)

        users = data['data']['usersByDevice']
        total_users = data['data']['aggregated']['registeredUsers']
        app_opens = data['data']['aggregated']['appOpens']

        for row in users:
            data_list.append({
                "Quarter": f"Q{i+1}",
                "Brand": row['brand'],
                "Count": row['count'],
                "Percentage": row['percentage'],
                "Total_Users": total_users,
                "App_Opens": app_opens
            })

    df = pd.DataFrame(data_list)

    # Sidebar filters
    st.sidebar.header("Filter Options")
    brand = st.sidebar.selectbox("Select Brand", df["Brand"].unique())
    quarter = st.sidebar.selectbox("Select Quarter", df["Quarter"].unique())

    filtered_df = df[
        (df["Brand"] == brand) & (df["Quarter"] == quarter)
    ]

    # KPIs
    st.subheader("📌 Key Metrics")
    col1, col2 = st.columns(2)

    col1.metric("Total Users", int(filtered_df["Total_Users"].mean()))
    col2.metric("App Opens", int(filtered_df["App_Opens"].mean()))

    # Line chart
    st.subheader("📈 Brand Trend Over Time")

    brand_df = df[df["Brand"] == brand]

    fig, ax = plt.subplots()
    ax.plot(brand_df["Quarter"], brand_df["Count"], marker='o')
    ax.set_title(f"{brand} Usage Trend")

    st.pyplot(fig)

    # Bar chart
    st.subheader("📊 Total Users by Brand")

    brand_total = df.groupby("Brand")["Count"].sum()

    st.bar_chart(brand_total)

    # Pie chart
    st.subheader("🥧 Market Share")

    fig2, ax2 = plt.subplots()
    df.groupby("Brand")["Percentage"].mean().plot(
        kind='pie', autopct='%1.1f%%', ax=ax2
    )
    st.pyplot(fig2)

    # Heatmap
    st.subheader("🔥 Heatmap")

    import seaborn as sns

    pivot = df.pivot_table(values="Count", index="Brand", columns="Quarter")

    fig3, ax3 = plt.subplots(figsize=(8,5))
    sns.heatmap(pivot, annot=True, ax=ax3)

    st.pyplot(fig3)

else:
    st.info("Please upload JSON files to view dashboard.")