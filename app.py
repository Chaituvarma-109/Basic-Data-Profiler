from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import seaborn as sns

st.set_page_config(layout='wide', )
st.title("Data Profiler")

hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)


def check_null_values(file_df=None):
    total_null_values = file_df.isna().sum()
    null_dict = {k: v for k, v in total_null_values.items() if v != 0}
    null_dict_df = pd.DataFrame(data=null_dict, index=[1])
    st.write(null_dict_df)


def describe_stats(file_df=None):
    st.dataframe(file_df.describe())


def file_viewer(file_df=None):
    if file_df:
        df = pd.read_csv(file_df)
        st.dataframe(df)
        return df


def main():
    file = st.sidebar.file_uploader("Upload a CSV file...")
    st.header("Data set")
    d_df = file_viewer(file_df=file)
    col1, col2 = st.columns(2)
    with st.container():
        with col1:
            st.header("Check for Null Values")
            check_null_values(file_df=d_df)
        with col2:
            st.header("Statistical Analysis of Data")
            describe_stats(file_df=d_df)
    st.header("Showing Correlation between Independent Features.")
    fig = plt.figure(figsize=(15, 10))
    sns.heatmap(data=d_df.corr(), annot=True, fmt='.2f')
    st.pyplot(fig)
    with st.container():
        st.header("Select the target or dependent column")
        option = st.selectbox(
            'Select the Dependent or target column',
            d_df.columns)
        target_col = d_df[option]
        independent_col = d_df.drop(columns=option)
        tar_col, ind_col = st.columns(2)
        with tar_col:
            st.subheader("Target Feature")
            st.dataframe(target_col)
        with ind_col:
            st.subheader("Independent Features")
            st.dataframe(independent_col)


if __name__ == "__main__":
    main()
