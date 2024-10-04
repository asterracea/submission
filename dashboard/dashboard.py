import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

day_df = pd.read_csv("../data/day.csv")
hour_df = pd.read_csv("../data/hour.csv")

day_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'cnt': 'count'
}, inplace=True)
# Mengganti tipe data di kolom dteday menjadi datetime pada dataframe day_df
day_df['dateday'] = pd.to_datetime(day_df['dateday'])

# mengubah nilai pada kolom weekday, month, year 
day_df['weekday'] = day_df['dateday'].dt.day_name()
day_df['year'] = day_df['dateday'].dt.year
day_df["month"] = day_df['dateday'].dt.month_name()

# mengubah nilai pada kolom season
day_df['season'] = day_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
# Weathersit column
day_df['weathersit'] = day_df['weathersit'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

#mengubah nama kolom
hour_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'cnt': 'count'
}, inplace=True)

# mengubah dteday menjadi datetime
hour_df["dateday"] = pd.to_datetime(hour_df["dateday"])

monthly_rent_df = day_df.resample(rule='M', on='dateday').agg({
    "casual": "sum",
    "registered": "sum",
    "count": "sum"
})
hour_df["year"] = hour_df['dateday'].dt.year
hour_df["month"] = hour_df['dateday'].dt.month_name()
hour_df["weekday"] = hour_df['dateday'].dt.day_name()

hour_df['season'] = hour_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
hour_df['weathersit'] = hour_df['weathersit'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})
monthly_rent_df = day_df.resample(rule='M', on='dateday').agg({
    "casual": "sum",
    "registered": "sum",
    "count": "sum"
})
# mengubah format menjadi bulan-tahun
monthly_rent_df.index = monthly_rent_df.index.strftime('%b-%y')
monthly_rent_df = monthly_rent_df.reset_index()

# Grouping bike renters (casual and registered) data by month
grouped_by_month = day_df.groupby('month')
aggregated_stats_by_month = grouped_by_month['count'].agg(['max', 'min', 'mean', 'sum'])


# Grouping bike renters (casual and registered) data by weather
grouped_by_weather = day_df.groupby('weathersit')
aggregated_stats_by_weather = grouped_by_weather['count'].agg(['max', 'min', 'mean', 'sum'])


# Grouping data by season and calculating aggregate statistics for temperature variables (temp),
# perceived temperature (atemp),
# and humidity (hum)
aggregated_stats_by_season = day_df.groupby('season').agg({
    'temp': ['max', 'min', 'mean'],
    'atemp': ['max', 'min', 'mean'],
    'hum': ['max', 'min', 'mean']
})

# Menyiapkan filter components (komponen filter)
min_date = day_df["dateday"].min()
max_date = day_df["dateday"].max()

st.sidebar.image("https://thumbs.dreamstime.com/z/bike-sharing-concept-city-transport-vector-illustration-bicycle-rental-service-mobile-application-ecological-road-trip-sporty-bike-215524703.jpg")
# Menampilkan header "Filter" di sidebar
st.sidebar.header("Filter:")
# Memilih rentang tanggal dengan date_input di sidebar
start_date, end_date = st.sidebar.date_input(
    label="Date",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Menambahkan pemisah horizontal di sidebar
st.sidebar.markdown("---")
st.header('Bike Sharing Dashboard :sparkles:')
# Menampilkan pemisah horizontal
st.markdown("---")
main_df = day_df[
    (day_df["dateday"] >= str(start_date)) &
    (day_df["dateday"] <= str(end_date))
]
# Membagi layar menjadi 3 kolom
col1, col2, col3 = st.columns(3)

# Menampilkan total rides di kolom pertama
with col1:
    total_all_rides = main_df['count'].sum()
    st.metric("Total Rides", value=total_all_rides)

# Menampilkan total casual rides di kolom kedua
with col2:
    total_casual_rides = main_df['casual'].sum()
    st.metric("Total Casual Rides", value=total_casual_rides)

# Menampilkan total registered rides di kolom ketiga
with col3:
    total_registered_rides = main_df['registered'].sum()
    st.metric("Total Registered Rides", value=total_registered_rides)

# Menampilkan pemisah horizontal
st.markdown("---")


#Visualisai
st.subheader("Bike Rental Trends in Recent Years")

monthly_rent_df['count'] = monthly_rent_df['casual'] + monthly_rent_df['registered']
fig = px.bar(monthly_rent_df,
             x='dateday',
             y=['casual', 'registered', 'count'],
             barmode='group',
             color_discrete_sequence=["#FF69B4", "#00FF00", "#0000FF"],
             labels={'casual': 'Casual Rentals', 'registered': 'Registered Rentals', 'count': 'Total Rides'})

fig.update_layout(xaxis_title='', yaxis_title='Total Rentals',
                  xaxis=dict(showgrid=False, showline=True, linecolor='rgb(204, 204, 204)', linewidth=2, mirror=True),
                  yaxis=dict(showgrid=False, zeroline=False, showline=True, linecolor='rgb(204, 204, 204)', linewidth=2, mirror=True),
                  plot_bgcolor='rgba(255, 255, 255, 0)',
                  showlegend=True,
                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

st.plotly_chart(fig, use_container_width=True)

#pertanyaan kedua
st.subheader("Bike Users Distribution Based on Weather Condition")
fig = px.box(day_df, x='weathersit', y='count', color='weathersit',
             labels={'weathersit': 'Weather Condition', 'count': 'Total Rentals'})
st.plotly_chart(fig, use_container_width=True)

#pertanyaan ketiga
st.subheader("What are the highest and lowest hours for bike usage")
sum_byhour_df = hour_df.groupby("hr")["count"].sum().sort_values(ascending=False).reset_index()
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

# First plot: Pelanggan Paling Sedikit
sns.barplot(
    x="hr", y="count", hue="hr",
    data=sum_byhour_df.sort_values(by="hr", ascending=True).head(5), 
    palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#72BCD4"], 
    ax=ax[0], legend=False
)
ax[0].set_ylabel(None)
ax[0].set_xlabel("Jam", fontsize=20)
ax[0].yaxis.set_label_position("right")
ax[0].set_title("Pelanggan Paling Sedikit", loc="center", fontsize=18)
ax[0].tick_params(axis='x', labelsize=20)
ax[0].tick_params(axis='y', labelsize=15)

# Second plot: Pelanggan Paling Banyak
sns.barplot(
    x="hr", y="count", hue="hr",
    data=sum_byhour_df.head(5), 
    palette=["#D3D3D3", "#D3D3D3", "#72BCD4", "#D3D3D3", "#D3D3D3"], 
    ax=ax[1], legend=False
)
ax[1].set_ylabel(None)
ax[1].set_xlabel("Jam", fontsize=20)
ax[1].set_title("Pelanggan Paling Banyak", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=20)
ax[1].tick_params(axis='y', labelsize=15)
ax[1].yaxis.tick_right()

plt.suptitle("Jumlah Pelanggan Berdasarkan Jam", fontsize=20)
st.pyplot(fig,use_container_width=True)
