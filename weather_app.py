import streamlit as st
import requests
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import statistics
from collections import Counter

# Set page config
st.set_page_config(page_title="Weather Forecast Dashboard", layout="wide", initial_sidebar_state="expanded")
    st.markdown("""
    ### 🌍 Try these example cities:
    - Kolkata, India
    - Delhi, India
    - Mumbai, India
    - New York, USA
    - London, UK
    - Tokyo, Japan
    """)
