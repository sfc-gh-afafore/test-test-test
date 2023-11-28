import os.path

import streamlit as st
import snowflake.connector
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def run():
    st.write(st.secrets)
    secret_file_path = st.secrets["connections"]["snowflake"]["private_key_file_path"]
    with open(secret_file_path, "rb") as key:
        p_key = serialization.load_pem_private_key(
            key.read(),
            password=None,
            backend=default_backend()
        )

    pkb = p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())

    conn = st.connection("snowflake", private_key=pkb)
    print("connected to snowflake!")
    data = conn.query('select * from FREE_DATASET_GZSNZ2UNRS.PUBLIC.CORE_POI limit 10;')
    selection = data[['STREET_ADDRESS', 'CITY', 'REGION', 'POSTAL_CODE', 'PHONE_NUMBER']]

    st.header('STARBUCKS LOCATIONS IN THE UNITED STATES')
    st.dataframe(selection)


if __name__ == "__main__":
    run()
