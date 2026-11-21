
import pandas as pd
import yfinance as yf


def get_crypto_data(symbol="BTCUSDT", interval="15m", limit=500):
    """Obtiene datos de criptomonedas desde Yahoo Finance."""

    symbol = symbol.upper()

    if symbol.endswith("USDT"):
        symbol = symbol[:-4] + "-USD"

    period = "60d" if interval in ["15m", "30m", "1h"] else "2y"

    df = yf.download(
        symbol,
        period=period,
        interval=interval,
        auto_adjust=True,
        progress=False
    )

    if df.empty:
        raise ValueError(f"No hay datos disponibles para {symbol}")

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()

    time_column = "Datetime" if "Datetime" in df.columns else "Date"
    df = df.rename(columns={time_column: "time"})
    df.columns = [str(c).lower() for c in df.columns]

    df = df[["time", "open", "high", "low", "close", "volume"]].copy()

    if interval == "4h":
        df = df.set_index("time").resample("4h").agg({
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum"
        }).dropna().reset_index()

    return df.tail(limit).reset_index(drop=True)


def get_stock_data(symbol="TSLA", interval="15m", period="60d"):
    """Obtiene datos de acciones desde Yahoo Finance."""

    download_interval = "1h" if interval == "4h" else interval

    df = yf.download(
        symbol.upper(),
        period=period,
        interval=download_interval,
        auto_adjust=True,
        progress=False
    )

    if df.empty:
        raise ValueError(f"No hay datos disponibles para {symbol}")

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()

    time_column = "Datetime" if "Datetime" in df.columns else "Date"
    df = df.rename(columns={time_column: "time"})
    df.columns = [str(c).lower() for c in df.columns]

    df = df[["time", "open", "high", "low", "close", "volume"]].copy()

    if interval == "4h":
        df = df.set_index("time").resample("4h").agg({
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum"
        }).dropna().reset_index()

    return df


def get_market_data(symbol, market="crypto", interval="15m"):
    """Selecciona la fuente según el mercado."""

    if market == "crypto":
        return get_crypto_data(symbol, interval)

    elif market == "stocks":
        return get_stock_data(symbol, interval)

    else:
        raise ValueError("Mercado no reconocido")

