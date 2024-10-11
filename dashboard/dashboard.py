
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the datasets (assuming the dataframes `day_df` and `hour_df` are already prepared)
@st.cache_data
def load_data():
    day_df = pd.read_csv('dashboard/day_data.csv')  # Replace with actual path or logic to load day data
    hour_df = pd.read_csv('dashboard/hour_data.csv')  # Replace with actual path or logic to load hour data
    return day_df, hour_df

day_df, hour_df = load_data()

# Dashboard Title and Introduction
st.title("Bike Sharing Data Analysis")
st.markdown('''
### Analyzing the relationship between weather conditions and bike rentals.
- How does weather affect daily bike rentals?
- How does apparent temperature impact hourly rentals?
''')

# Display Data
st.subheader("Dataset Preview")
if st.checkbox("Show Day Data"):
    st.write(day_df.head(10))

if st.checkbox("Show Hour Data"):
    st.write(hour_df.head(10))

# Data Visualization
st.subheader("Bike Rentals Over Time")
time_option = st.selectbox("Select Time Granularity", ("Daily", "Hourly"))

if time_option == "Daily":
    st.line_chart(day_df[['dteday', 'cnt']].set_index('dteday'))
else:
    st.line_chart(hour_df[['dteday', 'cnt']].set_index('dteday'))

# Weather-based Filtering
st.subheader("Filter by Weather Conditions")
weather_condition = st.radio("Select Weather Condition", day_df['weathersit'].unique())
filtered_data_weather = day_df[day_df['weathersit'] == weather_condition]

weather_rentals_filtered = filtered_data_weather.groupby("weathersit")["cnt"].mean().reset_index()

fig, ax = plt.subplots()
sns.lineplot(x="dteday", y="cnt", data=filtered_data_weather, ax=ax)
ax.set_title("Average Daily Bike Rentals by Weather Condition")
ax.set_xlabel("Date")
ax.set_ylabel("Average Rentals")
st.pyplot(fig)

# Temperature-based Filtering
st.subheader("Filter by Apparent Temperature Conditions")
temp_range = st.slider("Select Temperature Range", float(hour_df['atemp'].min()), float(hour_df['atemp'].max()), (10.0, 30.0))
filtered_data_atemp = hour_df[(hour_df['atemp'] >= temp_range[0]) & (hour_df['atemp'] <= temp_range[1])]

fig, ax = plt.subplots()
sns.lineplot(x="atemp", y="cnt", data=filtered_data_atemp, ax=ax)
ax.set_title("Bike Rentals vs Apparent Temperature (Hourly)")
ax.set_xlabel("Apparent Temperature (°C)")
ax.set_ylabel("Hourly Bike Rentals")
st.pyplot(fig)


# First question: Weather vs Daily Bike Rentals
st.subheader("Relationship between Weather and Daily Bike Rentals")
weather_rentals = day_df.groupby("weathersit")["cnt"].mean().reset_index()

fig, ax = plt.subplots(figsize=(20,12))
sns.barplot(x="weathersit", y="cnt", data=weather_rentals, ax=ax)
ax.set_title("Average Daily Bike Rentals by Weather Condition")
ax.set_xlabel("Weather Condition")
ax.set_ylabel("Average Rentals")
st.pyplot(fig)

# Second question: Apparent Temperature vs Hourly Bike Rentals
st.subheader("Relationship between Apparent Temperature and Hourly Bike Rentals")
fig, ax = plt.subplots()
sns.lineplot(x="atemp", y="cnt", data=hour_df, ax=ax)
ax.set_title("Bike Rentals vs Apparent Temperature (Hourly)")
ax.set_xlabel("Apparent Temperature (°C)")
ax.set_ylabel("Hourly Bike Rentals")
st.pyplot(fig)
