import pandas as pd
import matplotlib.pyplot as plt
# Define columns of interest
columns_to_use = ['date', 'location', 'total_cases', 'total_deaths', 'new_cases', 'new_deaths', 'total_vaccinations']

# Load the dataset with selected columns
df = pd.read_csv(r'C:\Users\Kabelo\OneDrive\Documents\Power Learn Program\Pyt[final project]\owid-covid-data.csv', usecols=columns_to_use)

# Filter for countries of interest
countries = ['Kenya', 'USA', 'India']
df = df[df['location'].isin(countries)]

# Drop rows with missing dates or critical values (date, location)
df = df.dropna(subset=['date', 'location'])

# Convert 'date' column to datetime type
df['date'] = pd.to_datetime(df['date'])

# Handle missing numeric values by interpolation (linear)
numeric_cols = ['total_cases', 'total_deaths', 'new_cases', 'new_deaths', 'total_vaccinations']
df[numeric_cols] = df[numeric_cols].interpolate(method='linear', limit_direction='both')

# Alternatively, if you prefer filling missing values with 0, you could use:
# df[numeric_cols] = df[numeric_cols].fillna(0)

# Preview the cleaned DataFrame
print("Cleaned dataset preview:")
print(df.head())

# Check for remaining missing values
print("\nMissing values after cleaning:")
print(df.isnull().sum())

# Plot total cases over time for selected countries

plt.figure(figsize=(12, 6))

for country in countries:

    subset = df[df['location'] == country]

    plt.plot(subset['date'], subset['total_cases'], label=country)

plt.title('Total COVID-19 Cases Over Time')

plt.xlabel('Date')

plt.ylabel('Total Cases')

plt.legend()

plt.grid(True)

plt.show()

# Plot total deaths over time for selected countries

plt.figure(figsize=(12, 6))

for country in countries:

    subset = df[df['location'] == country]

    plt.plot(subset['date'], subset['total_deaths'], label=country)

plt.title('Total COVID-19 Deaths Over Time')

plt.xlabel('Date')

plt.ylabel('Total Deaths')

plt.legend()

plt.grid(True)

plt.show()

# Compare daily new cases between countries

plt.figure(figsize=(12, 6))

for country in countries:

    subset = df[df['location'] == country]

    plt.plot(subset['date'], subset['new_cases'], label=country)

plt.title('Daily New COVID-19 Cases')

plt.xlabel('Date')

plt.ylabel('New Cases')

plt.legend()

plt.grid(True)

plt.show()


plt.rcParams['figure.figsize'] = (12, 6)

# --- Step 1: Ensure vaccination-related columns exist and are clean ---

vacc_cols = ['total_vaccinations', 'people_vaccinated', 'population']

for col in vacc_cols:

    if col not in df.columns:

        print(f"Warning: Column '{col}' not found in the dataset.")

    else:

        df[col] = pd.to_numeric(df[col], errors='coerce')

# Forward-fill population per country assuming it is relatively stable

if 'population' in df.columns:

    df.sort_values(['country', 'date'], inplace=True)

    df['population'] = df.groupby('country')['population'].ffill().bfill()

else:

    print("Warning: 'population' column missing. Some visualizations may be limited.")

# Fill missing vaccination data with 0 to ensure continuity

for col in ['total_vaccinations', 'people_vaccinated']:

    if col in df.columns:

        df[col] = df[col].fillna(0)

# Convert 'date' column to datetime

df['date'] = pd.to_datetime(df['date'], errors='coerce')

# --- Step 2: Plot cumulative vaccinations over time for selected countries ---

selected_countries = ['USA', 'India', 'Brazil']  # Customize as needed

plt.figure()

for country in selected_countries:

    country_data = df[df['country'] == country].sort_values('date')

    if not country_data.empty and 'total_vaccinations' in country_data.columns:

        plt.plot(country_data['date'], country_data['total_vaccinations'], marker='o', label=country)

    else:

        print(f"No cumulative vaccination data available for {country}.")

plt.title('Cumulative COVID-19 Vaccinations Over Time')

plt.xlabel('Date')

plt.ylabel('Total Vaccinations Administered')

plt.legend()

plt.xticks(rotation=45)

plt.tight_layout()




if all(col in df.columns for col in ['people_vaccinated', 'population']):

    df['pct_vaccinated'] = 0

    valid_pop = df['population'] > 0

    df.loc[valid_pop, 'pct_vaccinated'] = (df.loc[valid_pop, 'people_vaccinated'] / df.loc[valid_pop, 'population'] * 00)

    plt.figure()

    for country in selected_countries:

        country_data = df[df['country'] == country].sort_values('date')

        if not country_data.empty:

            plt.plot(country_data['date'], country_data['pct_vaccinated'], marker='o', label=country)

        else:

            print(f"No percentage vaccinated data available for {country}.")

    plt.title('Percentage of Population Vaccinated Over Time')

    plt.xlabel('Date')

    plt.ylabel('Percent Vaccinated (%)')

    plt.legend()

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()


    