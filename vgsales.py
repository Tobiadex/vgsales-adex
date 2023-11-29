from urllib.error import URLError
import streamlit as st 
import  numpy as np, pandas as pd 
import altair as alt

@st.cache_data
def get_data():
    path_= 'vgsales.csv'
    df = pd.read_csv(path_)
    # cleaning Year columns
    df.Year =df.Year.astype('str')
    df.Year = df.Year.str.replace('.0','')
    # cleaning publisher NAN
    df.dropna(inplace=True)
    return df

try:
    df = get_data()
    st.title(""" video games sales analysis """)
    st.dataframe(df.head(3))
    st.write(df.columns)
    # total sales metrics
    global_sales = np.round(np.sum(df.Global_Sales),2) 
    eu_sales = np.round(np.sum(df.EU_Sales),2)
    na_sales = np.round(np.sum(df.NA_Sales),2)
    jp_sales = np.round(np.sum(df.JP_Sales),2)
    other_sales = np.round(np.sum(df.Other_Sales),2)

    # create a ceries of columns 
    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)

   # card 
    col1.metric("Global sales Total",global_sales,"USD")
    col2.metric("Noth America sales",na_sales,"USD")
    col3.metric("European union sales",eu_sales,"USD")
    col4.metric("Japan sales Total",jp_sales,"USD")
    col5.metric("Other sales",other_sales,"USD")

    # filters
    col6, col7 = st.columns(2)
    platforms = df.Platform.unique()
    selected_platform = col6.multiselect(
        "Platfroms",platforms,[platforms[0],
                              platforms[1]]
    )
   
    # filters (genre)
    genre = df.Genre.unique()
    selected_genre = col7.multiselect(
        "Genre", genre,[genre[0], genre[1]]
    )
    filtered_data = df[df["Platform"].isin(selected_platform) &
                         df["Genre"].isin(selected_genre)]

    # table 
    if not selected_platform and selected_genre:
        st.error("please select both filters from platform and genre")

    st.write("""Filtered result""")
    st.table(filtered_data.head()) 

# table 

# plots 
# barchart 
    st.write(""" ## Global Sales per Platform """)
    bar1 = filtered_data.groupby(['Platform'])['Global_Sales'].sum().sort_values(ascending=True)
    st.write(bar1)
    st.bar_chart(bar1, color="#d4af37", width=200, height=400)
# line chart 
    st.write(""" ## Global sales over Time """)
    chart = (
         alt.Chart (filtered_data)
         .mark_line(opacity=0.8)
         .encode(
            x="Year",
            y=alt.Y("Global_Sales", stack=None),
         )
         
    )
    # AERA chart
    st.altair_chart(chart, use_container_width=True)
    st.write(""" ## Global sales over Time """)
    chart = (
         alt.Chart (filtered_data)
         .mark_area(opacity=0.8)
         .encode(
            x="Year",
            y=alt.Y("Global_Sales", stack=None),
         )
         
    )
    st.altair_chart(chart, use_container_width=True)
         #   "Choose countries", list(df.index), ["China", "United States of America"]
    # )
    # if not countries:
    #     st.error("Please select at least one country.")
    # else:
    #     data = df.loc[countries]
    #     data /= 1000000.0
    #     st.write("### Gross Agricultural Production ($B)", data.sort_index())

    #     data = data.T.reset_index()
    #     data = pd.melt(data, id_vars=["index"]).rename(
    #         columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
    #     )
    #     chart = (
    #         alt.Chart(data)
    #         .mark_area(opacity=0.3)
    #         .encode(
    #             x="year:T",
    #             y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
    #             color="Region:N",
    #         )
    #     )
    #     st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )
