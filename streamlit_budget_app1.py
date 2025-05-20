import streamlit as st
import json
import os

DATA_FILE = "web_budget_data.json"

# Load budget data from file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"allowance": 0, "saved": 0}

# Save budget data to file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Set page config
st.set_page_config(page_title="Budget Tracker", layout="centered")

# Custom iOS-style theming
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Helvetica Neue', sans-serif;
        background-color: #F4F6F8;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        max-width: 500px;
        margin: auto;
    }
    .stButton>button {
        background-color: #007AFF;
        color: white;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        border: none;
        font-size: 1rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #005FCC;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #007AFF;'>📲 Monthly Budget App</h1>", unsafe_allow_html=True)

data = load_data()

# Allowance input
st.subheader("💰 Monthly Allowance")
allowance = st.number_input("Enter your allowance for the month (R):", min_value=0.0, step=100.0, value=float(data["allowance"]))
data["allowance"] = allowance

if allowance > 0:
    # Suggestions
    suggested_save = round(allowance * 0.2, 2)
    suggested_spend = round(allowance * 0.8, 2)
    st.info(f"💡 Suggested split: Save **R{suggested_save}**, Spend **R{suggested_spend}**")

    # Add to savings
    st.subheader("🏦 Add to Savings")
    save_input = st.number_input("How much would you like to save this month?", min_value=0.0, step=50.0)

    if st.button("Add Savings"):
        data["saved"] += save_input
        st.success(f"✅ R{save_input:.2f} added to savings!")

    # Savings progress
    saved = data["saved"]
    goal = suggested_save
    progress = min(saved / goal, 1.0) if goal > 0 else 0

    st.subheader("📊 Savings Progress")
    st.progress(progress)
    st.metric("Saved", f"R{saved:.2f}")
    st.metric("Goal", f"R{goal:.2f}")
    st.metric("Remaining", f"R{max(0, goal - saved):.2f}")

else:
    st.warning("Please enter a monthly allowance to begin.")

save_data(data)
