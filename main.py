import streamlit as st
from datetime import date, timedelta
from utils import generate_travel_guide

banner_image_path = 'banner.png'

st.title("🌍 Travel Guide Generator")

st.image(banner_image_path, use_column_width=True)

with st.sidebar:
    openai_api_key = st.text_input("Enter OpenAI API Key:", type="password")
    st.markdown("[Get OpenAI API Key](https://platform.openai.com/account/api-keys)")

location = st.text_input("📍 Enter the travel location")

# Using date_input for the start and end dates of the travel duration
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("🛫 Start Date of Travel", min_value=date.today())

with col2:
    # 设置end_date的默认值为start_date之后的一天
    default_end_date = max(start_date + timedelta(days=1), date.today())
    end_date = st.date_input("🛬 End Date of Travel", min_value=start_date, value=default_end_date)

# Calculate the duration based on the start and end dates
duration = (end_date - start_date).days  # This will give the duration in days

budget = st.number_input("💰 Enter your budget in USD", min_value=1, step=100)
special_preferences = st.text_area("✨ Special Preferences (e.g., culture, food, activities)")

submit = st.button("Generate Travel Guide")

if submit:
    if not openai_api_key:
        st.error("Please enter your OpenAI API key.")
    elif not location:
        st.error("Please enter the travel location.")
    elif start_date > end_date:
        st.error("End date must be after the start date.")
    else:
        with st.spinner("Generating your personalized travel guide..."):
            # Pass the duration instead of the specific dates to the function
            travel_guide_content, wikipedia_info = generate_travel_guide(
                location, duration, budget, special_preferences, openai_api_key
            )

        st.subheader("✈️ Your Personalized Travel Guide:")
        st.write(travel_guide_content)

        # Display Wikipedia information in an expander
        with st.expander("📚 Wikipedia Information (click to expand)"):
            st.write(wikipedia_info)
