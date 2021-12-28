from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px

st.set_page_config(layout='wide', )
st.title("Data Profiler")

hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)


def box_plot(file_df, col):
    fig = px.box(data_frame=file_df, y=col)
    st.plotly_chart(fig, use_container_width=True)


def pair_plot(file_df):
    plt.figure()
    fig = sns.pairplot(file_df)
    st.pyplot(fig)


def correlation_plot(file_df):
    fig = plt.figure(figsize=(15, 10))
    sns.heatmap(data=file_df.corr(), annot=True, fmt='.2f')
    st.pyplot(fig)


def check_null_values(file_df=None):
    total_null_values = file_df.isna().sum()
    st.write(total_null_values[total_null_values > 0])


def describe_stats(file_df=None):
    st.dataframe(file_df.describe())


def file_viewer(file_df=None):
    if file_df:
        df = pd.read_csv(file_df)
        st.dataframe(df)
        return df


def main():
    file = st.sidebar.file_uploader("Upload a CSV file...")
    if file is not None:
        st.header("Data set")
        d_df = file_viewer(file_df=file)
        columns_df = d_df.columns
        col1, col2 = st.columns(2)
        with st.container():
            with col1:
                st.header("Check for Null Values")
                if st.button("check null values.."):
                    check_null_values(file_df=d_df)
            with col2:
                st.header("Statistical Analysis of Data")
                if st.button("Show Statistical Analysis.."):
                    describe_stats(file_df=d_df)
        with st.container():
            st.header("Showing Correlation between Independent Features.")
            if st.button("Show"):
                correlation_plot(d_df)
        with st.container():
            st.header("Select the target or dependent column")
            option = st.selectbox(
                'Select the Dependent or target column',
                columns_df)
            if st.button("Show target and independent features."):
                target_col = d_df[option]
                independent_col = d_df.drop(columns=option)
                tar_col, ind_col = st.columns(2)
                with tar_col:
                    st.subheader("Target Feature")
                    st.dataframe(target_col)
                with ind_col:
                    st.subheader("Independent Features")
                    st.dataframe(independent_col)
        with st.container():
            st.header("Showing the relationship between features")
            if st.button("Show the plot"):
                pair_plot(d_df)
        with st.container():
            st.header("Showing Outliers in the feature.")
            feature = st.selectbox(
                'select the feature or column to see the outliers.',
                d_df.columns
            )
            if st.button("Show outliers"):
                box_plot(d_df, feature)


if __name__ == "__main__":
    main()
