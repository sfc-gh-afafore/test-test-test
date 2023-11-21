import os.path

import streamlit as st
import snowflake.connector
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def run():
    private_key_path = os.path.join(os.getcwd(), 'dataset-credentials.p8')
    st.write(private_key_path)
    with open(private_key_path, "rb") as key:
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
        user=st.secrets["user"],
        account=st.secrets["account"],
        private_key=pkb,
    )
    print("connected to snowflake!")
    cur = conn.cursor()
    # conn = st.experimental_connection("snowpark", private_key=pkb, role="readonly_role")
    query = cur.execute('select * from free_dataset_GZ1M6Z2R41Y.public.t_rbaseit limit 10;');
    st.dataframe(query)


if __name__ == "__main__":
    run()
