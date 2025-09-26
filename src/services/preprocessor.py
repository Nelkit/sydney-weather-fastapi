import pandas as pd
import numpy as np


class DataPreprocessor():
    def __init__(self, data, hourly_vars, daily_vars):
        self.data = data
        self.hourly_vars = hourly_vars
        self.daily_vars = daily_vars

    def preprocess_weather_data(self):
        """Preprocess daily weather data focusing on precipitation metrics.

        Returns:
            pd.DataFrame: Processed daily weather data
        """
        response = self.data[0]
        print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation: {response.Elevation()} m asl")
        print(f"Timezone: {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

        # Process hourly data
        hourly = response.Hourly()
        hourly_variables = {var: idx for idx, var in enumerate(self.hourly_vars)}
        hourly_data = {"date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )}

        # Extract all hourly variables dynamically
        for var_name, idx in hourly_variables.items():
            hourly_data[var_name] = hourly.Variables(idx).ValuesAsNumpy()

        hourly_dataframe = pd.DataFrame(data=hourly_data)

        daily = response.Daily()
        daily_variables = {var: idx for idx, var in enumerate(self.daily_vars)}

        # Initialize daily data with date range
        daily_data = {"date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        )}

        # Extract all variables dynamically
        for var_name, idx in daily_variables.items():
            daily_data[var_name] = daily.Variables(idx).ValuesAsNumpy()

        daily_dataframe = pd.DataFrame(data=daily_data)

        # Create and return dataframe
        return hourly_dataframe, daily_dataframe

def aggregate_rain_or_not_dataframe(df_hourly, df_daily):
    """Aggregate hourly and daily dataframes to create features for rain or not prediction.

    Args:
        df_hourly (pd.DataFrame): Hourly weather data
        df_daily (pd.DataFrame): Daily weather data

    Returns:
        pd.DataFrame: Aggregated features dataframe
    """
    agg_dict = {
        "temperature_2m": ["mean", "min", "max", "std"],
        "dew_point_2m": ["mean", "min", "max"],
        "relative_humidity_2m": ["mean", "min", "max"],
        "precipitation": ["sum", "mean"],
        "rain": ["sum", "mean"],
        "wind_speed_10m": ["mean", "max"],
        "wind_gusts_10m": ["max"],
        "pressure_msl": ["mean", "min", "max"],
        "cloud_cover": ["mean", "max"],
        "cloud_cover_mid": ["mean", "max"],
        "cloud_cover_low": ["mean", "max"],
        "cloud_cover_high": ["mean", "max"],
        "surface_pressure": ["mean", "min", "max"],
        "vapour_pressure_deficit": ["mean", "max"],
        "boundary_layer_height": ["mean", "max"],
        "wet_bulb_temperature_2m": ["mean", "min", "max"],
        "total_column_integrated_water_vapour": ["mean", "max"]
    }

    df_hourly_agg = df_hourly.groupby("date").agg(agg_dict)
    df_hourly_agg.columns = ["h_" + "_".join(col).strip() for col in df_hourly_agg.columns]
    df_hourly_agg = df_hourly_agg.reset_index()

    # replace NaN values
    df_hourly_agg.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_hourly_agg.fillna(0, inplace=True)

    combined_df = pd.merge(df_hourly_agg, df_daily, on="date", how="inner")
    combined_df.fillna(0, inplace=True)

    return combined_df

def aggregate_precipitation_fall_dataframe(df_hourly, df_daily):
    """Aggregate hourly and daily dataframes to create features for precipitation fall prediction.

    Args:
        df_hourly (pd.DataFrame): Hourly weather data
        df_daily (pd.DataFrame): Daily weather data

    Returns:
        pd.DataFrame: Aggregated features dataframe
    """
    agg_dict = {
        "precipitation": ["sum", "mean"],
        "rain": ["sum", "mean"],
        "snowfall": ["sum"],
        "snow_depth": ["max"],
        "relative_humidity_2m": ["mean", "max", "min"],
        "dew_point_2m": ["mean", "min", "max"],
        "temperature_2m": ["mean", "min", "max", "std"],
        "apparent_temperature": ["mean", "min", "max", "std"],
        "cloud_cover": ["mean", "max"],
        "cloud_cover_high": ["mean"],
        "cloud_cover_mid": ["mean"],
        "cloud_cover_low": ["mean"],
        "pressure_msl": ["mean", "min", "max"],
        "surface_pressure": ["mean"],
        "wind_speed_10m": ["mean", "max"],
        "wind_speed_100m": ["mean", "max"],
        "wind_gusts_10m": ["max"],
        "soil_moisture_0_to_7cm": ["mean"],
        "soil_moisture_7_to_28cm": ["mean"],
    }

    df_hourly_agg = df_hourly.groupby("date").agg(agg_dict)
    df_hourly_agg.columns = ["h_" + "_".join(col).strip() for col in df_hourly_agg.columns]
    df_hourly_agg = df_hourly_agg.reset_index()

    df_weather_code = (
        df_hourly.groupby("date")["weather_code"]
        .agg(lambda x: x.mode()[0] if not x.mode().empty else None)
        .reset_index()
        .rename(columns={"weather_code": "h_weather_code"})
    )

    df_hourly_agg = df_hourly_agg.merge(df_weather_code, on="date", how="left")

    # replace NaN values
    df_hourly_agg.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_hourly_agg.fillna(0, inplace=True)

    combined_df = pd.merge(df_hourly_agg, df_daily, on="date", how="inner")

    return combined_df

