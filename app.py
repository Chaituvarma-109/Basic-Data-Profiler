import streamlit as st
import pandas as pd

st.set_page_config(layout='wide', )
st.title("Data Profiler")


def check_null_values(file_df=None):
    total_null_values = file_df.isna().sum()
    st.write(total_null_values)


def file_viewer(file_df=None):
    if file_df:
        df = pd.read_csv(file_df)
        st.dataframe(df)
        return df


def main():
    file = st.sidebar.file_uploader("Upload a CSV file...")
    st.header("Data set")
    df = file_viewer(file_df=file)
    st.header("Check for Null Values")
    check_null_values(file_df=df)
    ...


if __name__ == "__main__":
    main()
