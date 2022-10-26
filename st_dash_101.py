# Dependencies
import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine

# page styling
st.set_page_config(page_title="PLRA", page_icon=':bar_chart:', layout='wide')

# Connect to Database
engine = create_engine(
    'mssql+pyodbc://'
    'sa:MyPC:7390@AHMADBAYG\BAYGSSERVER/PLRA?' # username:pwd@server:port/database
    'driver=ODBC+Driver+17+for+SQL+Server'
    )

# ---- Connecting to Database ----
@st.cache
def get_data_from_db():
    # Connect to Database
    engine = create_engine(
        'mssql+pyodbc://'
        'sa:MyPC:7390@AHMADBAYG\BAYGSSERVER/PLRA?' # username:pwd@server:port/database
        'driver=ODBC+Driver+17+for+SQL+Server'
        )
    # Query Database
    df = pd.read_sql(
        'SELECT [Division]\
        ,[District]\
        ,[Tehsil]\
        ,[ARC_Name]\
        ,[Attendance]\
        ,[Mutation_Pendency]\
        ,[FARD_Issuance]\
        ,[Tokens_Information]\
        ,[Blockage]\
        ,[Total]\
        FROM [Scoring_Sheet_0]',
      engine
    )
    return df

df = get_data_from_db()


# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
division = st.sidebar.multiselect(
    "Select the Division:",
    options=df["Division"].unique(),
    default=df["Division"].unique()
)

# Performane_Params_list = ['Attendance', 'Mutation_Pendency', 'FARD_Issuance', 'Tokens_Information', 'Blockage']
# Performane_Params = st.sidebar.multiselect(
#     "Select the Performance Parameter:",
#     options=df[Performane_Params_list].unique(),
#     default=df[Performane_Params_list].unique(),
# )

# gender = st.sidebar.multiselect(
#     "Select the Gender:",
#     options=df["Gender"].unique(),
#     default=df["Gender"].unique()
# )

df_selection = df.query(
    "Division == @division"
    )
#  & Performance_Params_list ==@Performance_Params

# ---- MAINPAGE ----
st.title(":bar_chart:  ARCs Performance")
st.markdown("##")

# # TOP KPI's
# total_sales = int(df_selection["Total"].sum())
# average_rating = round(df_selection["Rating"].mean(), 1)
# star_rating = ":star:" * int(round(average_rating, 0))
# average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

# left_column, middle_column, right_column = st.columns(3)
# with left_column:
#     st.subheader("Total Sales:")
#     st.subheader(f"US $ {total_sales:,}")
# with middle_column:
#     st.subheader("Average Rating:")
#     st.subheader(f"{average_rating} {star_rating}")
# with right_column:
#     st.subheader("Average Sales Per Transaction:")
#     st.subheader(f"US $ {average_sale_by_transaction}")

# st.markdown("""---""")

# ----ARC Overall Score [BAR CHART]----
#df[df['Total']> 90].sort_values(by='Total', ascending=False)

top_df = (
    df_selection[df_selection['Total']> 95].sort_values(by='Total', ascending=False)
)

# fig_product_sales = px.bar(
#     sales_by_product_line,
#     x="Total",
#     y=sales_by_product_line.index,
#     orientation="h",
#     title="<b>Sales by Product Line</b>",
#     color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
#     template="plotly_white",
#)

fig_total = px.bar(
    top_df, x="ARC_Name",
    y="Total", 
    title="High Performers (Overall Score)",
    template="plotly_white"
)

fig_total.update_layout(
    plot_bgcolor="rgba(0,0,0,0)"
)

# ----ARC Score by Performance Parameters [BAR CHART]----

fig_all = px.bar(
    top_df, x="ARC_Name",
    y=["Attendance", "Mutation_Pendency", "FARD_Issuance", "Tokens_Information", "Blockage"],
    title="High Performers (Each Category)",
    labels={"variable": "Select to Filter Performance by Category:"}
)

fig_all.update_layout(
    plot_bgcolor="rgba(0,0,0,0)"
    #xaxis=(dict(showgrid=False))
)


# # SALES BY HOUR [BAR CHART]
# sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
# fig_hourly_sales = px.bar(
#     sales_by_hour,
#     x=sales_by_hour.index,
#     y="Total",
#     title="<b>Sales by hour</b>",
#     color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
#     template="plotly_white",
# )
# fig_hourly_sales.update_layout(
#     xaxis=dict(tickmode="linear"),
#     plot_bgcolor="rgba(0,0,0,0)",
#     yaxis=(dict(showgrid=False)),
# )


# left_column, right_column = st.columns(2)
# left_column.plotly_chart(fig_total, use_container_width=True)
# right_column.plotly_chart(fig_all, use_container_width=True)
st.plotly_chart(fig_total, use_container_width=True)
st.plotly_chart(fig_all, use_container_width=True)



# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)