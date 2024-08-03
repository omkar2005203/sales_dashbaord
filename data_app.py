import pandas as pd
import plotly.express as px
import streamlit as st

# Globals
container_width_size = True

st.set_page_config(page_title="Sales", page_icon=":bar_chart:", layout="wide")

@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io='supermarkt_sales.xlsx',
        engine='openpyxl',
        sheet_name="Sales",
        skiprows=3,
        usecols='B:R',
        nrows=1000
    )
    df['hour'] = pd.to_datetime(df['Time'], format="%H:%M:%S").dt.hour
    df['hour'] = df['hour'].astype(int)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = get_data_from_excel()

# Sidebar filters
st.sidebar.header("Filter")

city = st.sidebar.multiselect(
    "Select the city:",
    options=df['City'].unique(),
    default=df['City'].unique()
)

customer_type = st.sidebar.multiselect(
    "Select customer type:",
    options=df['Customer_type'].unique(),
    default=df['Customer_type'].unique()
)

gender = st.sidebar.multiselect(
    "Select gender:",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

st.dataframe(df_selection)

# Main page
st.title(":bar_chart: Sales")
st.markdown("##")

total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection['Rating'].mean(), 1)
star_rating = ":star:" * int(round(average_rating))
average_sale_transaction = round(df_selection["Total"].mean(), 2)

# Columns for KPIs
left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales}")

with middle_column:
    st.subheader("Average rating")
    st.subheader(f"{average_rating} {star_rating}")

with right_column:
    st.subheader("Average sale per transaction:")
    st.subheader(f"US $ {average_sale_transaction}")

st.markdown("---")

# Sales Trend Over Time
st.title("Sales Trend Over Time")
sales_trend = df_selection.groupby(by=[df_selection['Date'].dt.to_period("M")])['Total'].sum().reset_index()
sales_trend['Date'] = sales_trend['Date'].dt.to_timestamp()
st.line_chart(sales_trend, x='Date', y='Total')

# Columns for charts
left_col, right_col = st.columns(2)

# Sales by Product Line
with left_col:
    df_new_selection = df_selection.drop(['Date', 'Time'], axis=1)
    sales_by_product_line = df_new_selection.groupby(by=['Product line']).sum()[['Total']].sort_values("Total")
    st.title("Sales by Product Line")
    st.bar_chart(sales_by_product_line, horizontal=True, x_label='Total', y_label='Product line', use_container_width=container_width_size)

    # Sales by City
    sales_by_city = df_new_selection.groupby(by=['City']).sum()[['Total']]
    st.title("Sales by City")
    st.bar_chart(sales_by_city, x_label='City', y_label='Total', use_container_width=container_width_size)

    # Sales by Customer Type
    st.title("Sales by Customer Type")
    sales_by_customer_type = df_new_selection.groupby(by=['Customer_type']).sum()[['Total']]
    st.bar_chart(sales_by_customer_type, use_container_width=container_width_size)
    fig_customer_type_pie = px.pie(df_selection, names='Customer_type', values='Total', title='Sales Proportion by Customer Type')
    st.plotly_chart(fig_customer_type_pie, use_container_width=container_width_size)

# Sales by Hour
with right_col:
    df_selection = df_selection.drop(['Date', 'Time'], axis=1)
    sales_by_hour = df_selection.groupby(by=['hour']).sum()[['Total']]
    st.title("Sales by Hour")
    st.bar_chart(sales_by_hour, x_label='hour', y_label='Total', use_container_width=container_width_size)

    # Sales by Payment Method
    sales_by_payment = df_selection.groupby(by=['Payment']).sum()[['Total']]
    st.title("Sales by Payment Method")
    st.bar_chart(sales_by_payment, x_label='Payment Method', y_label='Total', use_container_width=container_width_size)

    # Sales by Gender
    st.title("Sales by Gender")
    sales_by_gender = df_selection.groupby(by=['Gender']).sum()[['Total']]
    st.bar_chart(sales_by_gender, use_container_width=container_width_size)
    fig_gender_pie = px.pie(df_selection, names='Gender', values='Total', title='Sales Proportion by Gender')
    st.plotly_chart(fig_gender_pie, use_container_width=container_width_size)

# Hide Streamlit style
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
