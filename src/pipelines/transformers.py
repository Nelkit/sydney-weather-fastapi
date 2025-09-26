import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


# WEATHER CODE TRANSFORMER
class WeatherCodeTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, feature_name="weather_code", output_name="weather_category"):
        self.feature_name = feature_name
        self.output_name = output_name
        self.weather_category_map = {
            0: "Clear",
            1: "Cloudy", 2: "Cloudy", 3: "Cloudy",
            45: "Fog", 48: "Fog",
            51: "Drizzle", 53: "Drizzle", 55: "Drizzle",
            56: "Freezing Drizzle", 57: "Freezing Drizzle",
            61: "Rain", 63: "Rain", 65: "Rain",
            66: "Freezing Rain", 67: "Freezing Rain",
            71: "Snow", 73: "Snow", 75: "Snow",
            77: "Snow Grains",
            80: "Rain Showers", 81: "Rain Showers", 82: "Rain Showers",
            85: "Snow Showers", 86: "Snow Showers",
            95: "Thunderstorm",
            96: "Thunderstorm with Hail", 99: "Thunderstorm with Hail"
        }

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()
        df[self.output_name] = df[self.feature_name].map(self.weather_category_map).fillna("Unknown")
        return df


# DATE FEATURES TRANSFORMER
class DateFeaturesTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()
        df["date"] = pd.to_datetime(df["date"])
        df["day_of_week"] = df["date"].dt.weekday
        df["day_of_year"] = df["date"].dt.dayofyear
        df["month"] = df["date"].dt.month
        df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)
        df["sin_day_of_year"] = np.sin(2 * np.pi * df["day_of_year"] / 365)
        df["cos_day_of_year"] = np.cos(2 * np.pi * df["day_of_year"] / 365)
        return df


# SEASON FEATURES TRANSFORMER
def month_to_season_sydney(month):
    if month in [12, 1, 2]:
        return "Summer"
    elif month in [3, 4, 5]:
        return "Autumn"
    elif month in [6, 7, 8]:
        return "Winter"
    else:
        return "Spring"


class SeasonFeaturesTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()
        if "month" not in df.columns:
            raise ValueError("Missing 'month' column. Run DateFeaturesTransformer first.")
        df["season"] = df["month"].apply(month_to_season_sydney)
        return df


# RAIN LAG FEATURES
class RainLagTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, lags=[1, 2, 3, 7, 14]):
        self.lags = lags

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()
        for lag in self.lags:
            df[f"rain_sum_in_{lag}d"] = df["rain_sum"].shift(lag).fillna(0)
        return df


# RAIN ROLLING FEATURES
class RainRollingTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, windows=[3, 7, 14]):
        self.windows = windows

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()
        for window in self.windows:
            df[f"rain_sum_in_{window}d"] = df["rain_sum"].rolling(window=window).sum().fillna(0)
        return df

# TEMPERATURE & HUMIDITY TRANSFORMER
class TempHumidityTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()

        df["temperature_range"] = (df["temperature_2m_max"] - df["temperature_2m_min"]).fillna(0)
        df["humidity_range"] = (df["relative_humidity_2m_max"] - df["relative_humidity_2m_min"]).fillna(0)
        df["dew_point_gap"] = (df["h_dew_point_2m_mean"] - df["dew_point_2m_mean"]).fillna(0)

        df["vpd_ratio"] = (df["h_vapour_pressure_deficit_max"] /
                           df["h_vapour_pressure_deficit_mean"].replace(0, np.nan)).fillna(0)

        df["apparent_temperature"] = (
            df["temperature_2m_mean"]
            + 0.33 * df["relative_humidity_2m_mean"]
            - 0.7 * df["h_wind_speed_10m_max"]
            - 4
        ).fillna(0)

        return df


# WIND FEATURES TRANSFORMER
class WindFeaturesTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()

        df["wind_diff"] = (df["h_wind_speed_10m_max"] - df["wind_speed_10m_max"]).fillna(0)

        wind_dir_rad = np.radians(df["wind_direction_10m_dominant"].fillna(0))
        df["wind_u"] = (df["wind_speed_10m_mean"] * np.cos(wind_dir_rad)).fillna(0)
        df["wind_v"] = (df["wind_speed_10m_mean"] * np.sin(wind_dir_rad)).fillna(0)

        df["wind_rain_interaction"] = (df["wind_speed_10m_max"] * df["rain_sum"].fillna(0)).fillna(0)

        return df




# CYCLICAL FEATURES TRANSFORMER
class CyclicalFeaturesTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()
        if "day_of_week" in df.columns:
            df["day_of_week_sin"] = np.sin(2 * np.pi * df["day_of_week"] / 7)
            df["day_of_week_cos"] = np.cos(2 * np.pi * df["day_of_week"] / 7)
        if "day_of_year" in df.columns:
            df["day_of_year_sin"] = np.sin(2 * np.pi * df["day_of_year"] / 365)
            df["day_of_year_cos"] = np.cos(2 * np.pi * df["day_of_year"] / 365)
        if "month" in df.columns:
            df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
            df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
        return df


# Multilag Features Transformer
class MultiLagTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, lag_vars=None, lag_days=None, fillna_value=0):
        """
        Parameters
        ----------
        lag_vars : list of str
            List of variable names to generate lag features for.
        lag_days : list of int
            List of lags (in days) to apply.
        fillna_value : int or float, default=0
            Value to fill NaNs generated by shifting.
        """
        self.lag_vars = lag_vars if lag_vars is not None else []
        self.lag_days = lag_days if lag_days is not None else [1, 3, 7]
        self.fillna_value = fillna_value
        self.new_features_ = []

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()
        self.new_features_ = []

        for var in self.lag_vars:
            if var not in df.columns:
                raise ValueError(f"Column '{var}' not found in input DataFrame")
            for lag in self.lag_days:
                col_name = f"{var}_lag{lag}"
                df[col_name] = df[var].shift(lag).fillna(self.fillna_value)
                self.new_features_.append(col_name)

        return df


class RollingFeaturesTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, rolling_vars=None, rolling_windows=None, rolling_stats=None, fillna_value=0):
        """
        Parameters
        ----------
        rolling_vars : list of str
            Variables sobre las que calcular rolling windows.
        rolling_windows : list of int
            Tamaños de ventanas (en días).
        rolling_stats : list of str
            Estadísticas a calcular: 'mean', 'max', 'min', 'std', etc.
        fillna_value : int or float, default=0
            Valor para reemplazar NaNs producidos por las ventanas.
        """
        self.rolling_vars = rolling_vars if rolling_vars is not None else []
        self.rolling_windows = rolling_windows if rolling_windows is not None else [3, 7]
        self.rolling_stats = rolling_stats if rolling_stats is not None else ["mean", "max", "min"]
        self.fillna_value = fillna_value
        self.new_features_ = []

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()
        self.new_features_ = []

        for var in self.rolling_vars:
            if var not in df.columns:
                raise ValueError(f"Column '{var}' not found in DataFrame")

            for window in self.rolling_windows:
                roll = df[var].rolling(window=window)

                for stat in self.rolling_stats:
                    col_name = f"{var}_{window}d_{stat}"

                    if stat == "mean":
                        df[col_name] = roll.mean()
                    elif stat == "max":
                        df[col_name] = roll.max()
                    elif stat == "min":
                        df[col_name] = roll.min()
                    elif stat == "std":
                        df[col_name] = roll.std()
                    else:
                        raise ValueError(f"Statistic '{stat}' not implemented")

                    df[col_name] = df[col_name].fillna(self.fillna_value)
                    self.new_features_.append(col_name)

        return df

def num_selector(df):
    return df.select_dtypes(include='number').columns.tolist()

def cat_selector(df):
    return df.select_dtypes(include='object').columns.tolist()