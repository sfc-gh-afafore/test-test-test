import os.path

import streamlit as st
import snowflake.connector
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def run():
    secret_file_path = st.secrets["connections"]["snowflake"]["private_key_file_path"]
    st.write(secret_file_path)
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

    conn = snowflake.connector.connect(
        user=st.secrets["connections"]["snowflake"]["user"],
        account=st.secrets["connections"]["snowflake"]["account"],
        database="FREE_DATASET_GZT0ZLVIV74",
        warehouse=st.secrets["connections"]["snowflake"]["warehouse"],
        role=st.secrets["connections"]["snowflake"]["role"],
        private_key=pkb,
    )
    print("connected to snowflake!")
    cur = conn.cursor()
    # conn = st.experimental_connection("snowpark", private_key=pkb, role="readonly_role")
    query = cur.execute('select * from FREE_DATASET_GZT0ZLVIV74.PUBLIC.HH_PET_202209 limit 10;');
    st.dataframe(query)


if __name__ == "__main__":
    run()
