import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuration of the dashboard
st.set_page_config(page_title="Testing Streamlit Homework 1", layout="wide")
st.title("Sales Interface")
st.markdown("The following dashboard will help you visualize graphs of Units Sold, Total Sales, and Average Sales.")

# Here we select our data and visualize it 
data=pd.read_csv('sellers.csv', encoding = 'utf-8-sig')

st.dataframe(data)

# We add a filter
st.sidebar.header("Filters")

# We add the filter per Region
regions = data["REGION"].unique()
selected_region = st.sidebar.selectbox("Choose a Region", ["Todas"] + list(regions))

if selected_region != "Todas":
    filtered_data = data[data["REGION"] == selected_region]
else:
    filtered_data = data

# Filter per Vendor
vendors = filtered_data["NAME"] + " " + filtered_data["LASTNAME"]
selected_vendor = st.sidebar.selectbox("Choose a vendor", ["Todos"] + vendors.tolist())

if selected_vendor != "Todos":
    filtered_data = filtered_data[(filtered_data["NAME"] + " " + filtered_data["LASTNAME"]) == selected_vendor]

# View of the filter table
st.subheader("New Table")
st.dataframe(filtered_data, use_container_width=True)

# Grahps
with st.container():
    st.subheader("General Indicators")

    col1, col2, col3 = st.columns(3)

    # Units sold
    col1.metric("Total Units Sold", f"{filtered_data['SOLD UNITS'].sum():,}")

    # Total Sales
    col2.metric("Total Sales", f"${filtered_data['TOTAL SALES'].sum():,}")

    # Average Sales
    col3.metric("Average Sales", f"{filtered_data['SALES AVERAGE'].mean():.2f}")

st.subheader("Display")

# Here we create the bottons for the graphs asked
chart_type = st.radio(
    "Select a graph to view",
    ["Units Sold", "Total Sales", "Average Sales"],
    horizontal=True
)

fig, ax = plt.subplots(figsize=(8, 4))

if chart_type == "Units Sold":
    ax.bar(filtered_data["NAME"], filtered_data["SOLD UNITS"], color="blue")
    ax.set_title("Units Sold per vendor")
    ax.set_ylabel("Units Sold")
    plt.xticks(rotation=45, ha='right', fontsize=6)
    plt.tight_layout()

elif chart_type == "Total Sales":
    ax.bar(filtered_data["NAME"], filtered_data["TOTAL SALES"], color="grey")
    ax.set_title("Total Sales per vendor")
    ax.set_ylabel("Total Sales ($)")
    plt.xticks(rotation=45, ha='right', fontsize=6)
    plt.tight_layout()

elif chart_type == "Average Sales":
    ax.bar(filtered_data["NAME"], filtered_data["SALES AVERAGE"], color="black")
    ax.set_title("Average Sales per vendor")
    ax.set_ylabel("Sales Average")
    plt.xticks(rotation=45, ha='right', fontsize=6)
    plt.tight_layout()

st.pyplot(fig)

# Finally we show the data of an specific vendor
if selected_vendor != "Todos":
    st.subheader(f"details of {selected_vendor}")
    vendor_row = data[(data["NAME"] + " " + data["LASTNAME"]) == selected_vendor].iloc[0]
    st.write(f"**Región:** {vendor_row['REGION']}")
    st.write(f"**Ingreso:** ${vendor_row['INCOME']:,}")
    st.write(f"**Unidades vendidas:** {vendor_row['SOLD UNITS']}")
    st.write(f"**Total de ventas:** ${vendor_row['TOTAL SALES']:,}")
    st.write(f"**Promedio de ventas:** {vendor_row['SALES AVERAGE']:.2f}")
