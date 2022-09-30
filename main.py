import streamlit as st
from gsheetsdb import connect

# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

st.title("SinfuL Artificial Intelligence")
st.text("Welcome to my game, good luck trying to stop me..")
st.text("If you feed me the right answer, I'll tell you where to look next.")

# Answer and clue output
answers = st.text_input("Answer", placeholder="what have you got for me?", help="Enter in the right answer, and your next clue will appear.").lower()
if st.button("Submit"):
    for row in rows:
        if answers in row:
            st.write(row.clue)
            break
    else:
        st.write("Sorry, that doesn't mean anything to me.. ")
