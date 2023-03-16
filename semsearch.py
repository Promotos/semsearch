import streamlit as st
import time
import sys

# Check root directory argument available
if len(sys.argv) == 1:
    raise Exception("Please provide a root directory as start argument.")
else:
    root_dir = sys.argv[1]

# Display progress on index creation
progress_text = str(root_dir) +  " Operation in progress. Please wait."
placeholder = st.empty()
my_bar = placeholder.progress(0, text=progress_text)

for percent_complete in range(100):
    time.sleep(0.1)
    my_bar.progress(percent_complete + 1, text=progress_text + str(percent_complete))


# Remove progress component an replace with search components
placeholder.empty()
st.write("done")