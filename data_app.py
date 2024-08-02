import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales",page_icon=":bar_chart:",layout="wide")


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

    df['hour'] = pd.to_datetime(df['Time'],format="%H:%M:%S").dt.hour
    df['hour'] = df['hour'].astype(int)
    print(df)

    return df


df = get_data_from_excel()
# st.dataframe(df)

# side bar

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

print(f"values : {city}  {customer_type} {gender}")
df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

st.dataframe(df_selection)



# mainpage

st.title(":bar_chart: Sales")
st.markdown("##")

total_sales = int(df_selection["Total"].sum())

average_rating = round(df_selection['Rating'].mean(),1)

star_rating = ":star:"*int(round(average_rating))

average_sale_transaction = round(df_selection["Total"].mean(),2)

#columns

left_column,middle_column,right_column = st.columns(3)

with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales}")

with middle_column:
    st.subheader("Average rating ")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average sale per transaction:")
    st.subheader(f"US $ {average_sale_transaction}")


st.markdown("---")

# columns
left_col,rigth_col = st.columns(2)


# sales by product line
with left_col:
    df_new_selection = df_selection.drop(['Date','Time'], axis=1)
    sales_by_product_line  = df_new_selection.groupby(by=['Product line']).sum()[['Total']].sort_values("Total")
    st.title("Sales by product line")
    st.bar_chart(sales_by_product_line,horizontal=True,x_label='Total',y_label='Product line',use_container_width=True)

    print(sales_by_product_line)

# sales by hour
with rigth_col:
    print(df_selection.dtypes)
    df_selection = df_selection.drop(['Date','Time'],axis=1)
    df_selection['hour'] = df_selection['hour'].astype(int)
    sales_by_hour = df_selection.groupby(by=['hour']).sum()[['Total']]
    st.title("Sales by hour")
    st.bar_chart(sales_by_hour,x_label='hour',y_label='Total',use_container_width=True)

    print(sales_by_hour)



# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)