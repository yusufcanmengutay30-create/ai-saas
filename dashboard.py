import streamlit as st
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///data/app.db")

st.title("🚀 AI Content Factory v8")

user = st.text_input("User name")

if st.button("Load History"):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM logs WHERE user=:u ORDER BY id DESC"),
            {"u": user}
        )

        for row in result:
            st.subheader(f"Model: {row.model}")
            st.write(row.prompt)
            st.write(row.output)
            st.write("---")
