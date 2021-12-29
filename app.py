from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px

st.set_page_config(layout='wide', )
st.title("Data Profiler")

# #MainMenu {visibility: hidden;}
hide_st_style = """
<style>
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)


def box_plot(file_df, col):
    fig = px.box(data_frame=file_df, y=col)
    st.plotly_chart(fig)


def bar_plot(file_df, lst_cols):
    fig = px.bar(file_df, x=lst_cols[0], y=lst_cols[1])
    st.plotly_chart(fig)


def correlation_plot(file_df):
    fig = plt.figure(figsize=(10, 5))
    sns.heatmap(data=file_df.corr(), annot=True, fmt='.2f')
    st.pyplot(fig)


@st.cache
def check_null_values(file_df):
    total_null_values = file_df.isna().sum()
    null_df = total_null_values[total_null_values > 0]
    return null_df


@st.cache
def describe_stats(file_df):
    des = file_df.describe()
    return des


@st.cache
def file_viewer(file_df):
    df = pd.read_csv(file_df)
    return df


def main():
    file = st.sidebar.file_uploader("Upload a CSV file...")

    if file is not None:
        st.header("Data set")
        d_df = file_viewer(file)
        st.dataframe(d_df)
        columns_df = d_df.columns
        col1, col2 = st.columns(2)
        # Checking Null values and shows Statistical Analysis
        with st.container():
            with col1:
                st.header("Check for Null Values")
                null_values = st.button("check null values..")
                if "null_state" not in st.session_state:
                    st.session_state.null_state = False
                if null_values or st.session_state.null_state:
                    st.session_state.null_state = True
                    null_df = check_null_values(d_df)
                    if null_df.any():
                        st.dataframe(null_df)
                    else:
                        st.info("There are No NULL or NAN values.")
            with col2:
                st.header("Statistical Analysis of Data")
                stat = st.button("Show Statistical Analysis..")
                if "stat_state" not in st.session_state:
                    st.session_state.stat_state = False
                if stat or st.session_state.stat_state:
                    st.session_state.stat_state = True
                    stat_df = describe_stats(d_df)
                    st.dataframe(stat_df)
        # Showing correlation maps
        with st.container():
            st.header("Showing Correlation between Independent Features.")
            corr_plot = st.button("Show")
            if "corr_state" not in st.session_state:
                st.session_state.corr_state = False
            if corr_plot or st.session_state.corr_state:
                st.session_state.corr_state = True
                correlation_plot(d_df)
        # Showing Pair plots
        with st.container():
            st.header("Showing the relationship between features")
            plot_feature = st.multiselect(
                'Select any Two features to See realtionship between them',
                columns_df,
            )
            if "pair_state" not in st.session_state:
                st.session_state.pair_state = False
            if plot_feature or st.session_state.pair_state:
                st.session_state.pair_state = True
                bar_plot(d_df, plot_feature)
        # Checking the outliers using box plots
        with st.container():
            st.header("Showing Outliers in the feature.")
            feature = st.selectbox(
                'select the feature or column to see the outliers.',
                columns_df
            )
            if "outlier_feature" not in st.session_state:
                st.session_state.outlier_feature = False
            if feature or st.session_state.outlier_feature:
                st.session_state.outlier_feature = True
                box_plot(d_df, feature)
    else:
        st.info("Upload the CSV file....")


if __name__ == "__main__":
    main()
