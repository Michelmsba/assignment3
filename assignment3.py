import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Data Visualizations", layout="wide")

# Introduction and context
st.title("Interactive Data Visualizations")
st.write("""
    This page presents two interactive visualizations derived from the dataset: consumer price indices in Lebanon. The first visualization is a line chart shows the trend of the prices over the years (inflation), 
    while the second explores how these prices change across different months of the year. To enhance interactivity, the page contains three interactive feactures that affect the visualizations. The first two features,
    impact the first and second visual where the users can choose the year range and value range according to their interests. Also, a third feature affects only the second visual where they can choose a year, and the
    corresponding values for its corresponding months will be displayed.
""")

# Load and clean data
df = pd.read_csv("14b89103253820add272eacabd0604d6_20240909_192340.csv")
df_cleaned = df[df['EndDate'] != '#date+end']
df_cleaned['EndDate'] = pd.to_datetime(df_cleaned['EndDate'], errors='coerce')
df_cleaned = df_cleaned.dropna(subset=['EndDate'])
df_cleaned['Value'] = pd.to_numeric(df_cleaned['Value'], errors='coerce')
df_cleaned = df_cleaned.dropna(subset=['Value'])
df_cleaned['Year'] = df_cleaned['EndDate'].dt.year
df_cleaned['Month'] = df_cleaned['EndDate'].dt.month_name()

# Create the first visualization: Yearly average values
df_yearly = df_cleaned[['Year', 'Value']].groupby('Year').mean().reset_index()

# Add interactive filters
st.sidebar.header("Filters")
year_range = st.sidebar.slider("Select Year Range", int(df_cleaned['Year'].min()), int(df_cleaned['Year'].max()), 
                               (int(df_cleaned['Year'].min()), int(df_cleaned['Year'].max())))

# Limit the value range to a maximum of 7000
value_range = st.sidebar.slider("Select Value Range", int(df_cleaned['Value'].min()), 15000, 
                                (int(df_cleaned['Value'].min()), min(15000, int(df_cleaned['Value'].max()))))

# Filter data based on the selected ranges
filtered_data = df_cleaned[(df_cleaned['Year'].between(year_range[0], year_range[1])) & 
                           (df_cleaned['Value'].between(value_range[0], value_range[1]))]

# Update the yearly data for the first chart
df_yearly_filtered = filtered_data[['Year', 'Value']].groupby('Year').mean().reset_index()

# First visualization: Line chart (Value Trend Over the Years)
st.subheader("Inflation Rate in Lebanon Over the Years")
line_chart_yearly = px.line(df_yearly_filtered, x='Year', y='Value', title="Inflation Rate in Lebanon the Selected Years",
                            range_y=[df_cleaned['Value'].min(), min(15000, df_cleaned['Value'].max())])
st.plotly_chart(line_chart_yearly, use_container_width=True)
# Description of the insights
st.subheader("Insights of the Bar Chart")
st.write("""
    This line chart visualizes the inflation rate in Lebanon over the selected years. The data represents the average value 
    for each year, and by adjusting the filters on the sidebar, you can explore how inflation fluctuated across different 
    time periods. The y-axis is limited to a maximum of 15,000 to make the visualization clearer and more interpretable.
    By analyzing the visual, we can notice a very clear insight which is the sharp increase in the inflation rate after 
    2019. Before that, the fluctuation was very low. This is directly linked to the economic crisis that started in 2019,
    in addition to the international inflation due to the Covid Pandemic. 
""")
# Pagination: Display each year on a separate page
all_years = sorted(filtered_data['Year'].unique())
selected_year = st.sidebar.selectbox('Select Year', all_years)

# Filter data for the selected year
filtered_year_data = filtered_data[filtered_data['Year'] == selected_year]

# Create the second visualization: Monthly average values for the selected year
df_monthly_yearly = filtered_year_data[['Month', 'Value']].groupby('Month').mean().reset_index()

# Sort months correctly (optional, for aesthetic purposes)
df_monthly_yearly['Month'] = pd.Categorical(df_monthly_yearly['Month'], 
                                     categories=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 
                                                 'September', 'October', 'November', 'December'], ordered=True)
df_monthly_yearly = df_monthly_yearly.sort_values('Month')

# Second visualization: Bar chart (Monthly Average Values for the Selected Year)
st.subheader(f"Average Inflation Rate by Month for {selected_year}")
bar_chart_monthly_yearly = px.bar(df_monthly_yearly, x='Month', y='Value', title=f"Average Inflation Rate by Month for {selected_year}",
                                  range_y=[df_cleaned['Value'].min(), min(3000, df_cleaned['Value'].max())])
st.plotly_chart(bar_chart_monthly_yearly, use_container_width=True)

# Insights section
st.subheader("Insights of the Bar Chart")
st.write(f"""
    This Visual is more specific than the first one, because it shows the fluctuations in each year within its months. By analyzing
    several years, i noticed that the general trend between the months in each year is increasing year after year. The most clear one 
    is in 2020 and 2021, where the inflation is sharply increasing each month from January to December. 
""")
