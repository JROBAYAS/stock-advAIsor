import yfinance as yf

def fetch_stock_summary(ticker):
    t = yf.Ticker(ticker)
    # Obtener los últimos 5 días para asegurar que tenemos datos suficientes
    data = t.history(period="5d")
    
    # Verificar que tenemos al menos 2 días de datos
    if len(data) < 2:
        return {
            "price": data["Close"].iloc[-1] if len(data) > 0 else 0,
            "change": 0,
        }

    last_price = data["Close"].iloc[-1]
    prev_price = data["Close"].iloc[-2]
    change = ((last_price - prev_price) / prev_price) * 100

    return {
        "price": last_price,
        "change": round(change, 2),
    }
