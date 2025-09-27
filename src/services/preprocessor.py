import pandas as pd
import numpy as np


class DataPreprocessor():
    def __init__(self, data, hourly_vars, daily_vars):
        self.data = data
        self.hourly_vars = hourly_vars
        self.daily_vars = daily_vars

    def preprocess_weather_data(self):
        """Preprocess Open-Meteo JSON into hourly and daily DataFrames.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: (hourly_dataframe, daily_dataframe)
        """
        payload = self.data

        # Hourly data
        hourly_payload = payload.get("hourly", {})
        hourly_times = hourly_payload.get("time", [])
        hourly_dataframe = pd.DataFrame()
        if hourly_times:
            hourly_dataframe["date"] = pd.to_datetime(hourly_times, utc=True)
        else:
            hourly_dataframe["date"] = pd.to_datetime([])

        for var_name in self.hourly_vars:
            values = hourly_payload.get(var_name)
            # Ensure column exists even if missing from response
            hourly_dataframe[var_name] = values if values is not None else pd.Series([pd.NA] * len(hourly_dataframe))

        # Daily data
        daily_payload = payload.get("daily", {})
        daily_times = daily_payload.get("time", [])
        daily_dataframe = pd.DataFrame()
        if daily_times:
            # Daily dates are at midnight; parse as date-time for consistency
            daily_dataframe["date"] = pd.to_datetime(daily_times, utc=True)
        else:
            daily_dataframe["date"] = pd.to_datetime([])

        for var_name in self.daily_vars:
            values = daily_payload.get(var_name)
            daily_dataframe[var_name] = values if values is not None else pd.Series([pd.NA] * len(daily_dataframe))

        return hourly_dataframe, daily_dataframe

def join_rain_data(df_daily, df_hourly):
    df_daily["date"] = pd.to_datetime(df_daily["date"]).dt.normalize()
    df_hourly["date"] = pd.to_datetime(df_hourly["date"]).dt.normalize()

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

    df_combined = pd.merge(df_daily, df_hourly_agg, on="date", how="inner")

    return df_combined

def join_precipitation_data(df_daily, df_hourly):
    df_daily["date"] = pd.to_datetime(df_daily["date"]).dt.normalize()
    df_hourly["date"] = pd.to_datetime(df_hourly["date"]).dt.normalize()

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

    daily_cols = [col for col in df_daily.columns if col != "date"]
    df_daily_renamed = df_daily.rename(columns={col: f"d_{col}" for col in daily_cols})

    df_combined = pd.merge(df_daily_renamed, df_hourly_agg, on="date", how="inner")

    return df_combined

