import os.path

import streamlit as st
import snowflake.connector
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def run():
    conn = st.connection("snowflake")
    st.write("Connection Successful!")
    data = conn.query('select * from FREE_DATASET_GZSNZ2UNRS.PUBLIC.CORE_POI limit 10;')
    selection = data[['STREET_ADDRESS', 'CITY', 'REGION', 'POSTAL_CODE', 'PHONE_NUMBER']]

    st.header('STARBUCKS LOCATIONS IN THE UNITED STATES')
    st.dataframe(selection)


if __name__ == "__main__":
    run()
