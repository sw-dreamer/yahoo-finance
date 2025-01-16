import yfinance as yf
import sys
import json
from datetime import datetime, timedelta

def fetch_stock_data(stock_symbol):
    # 2년 전 날짜를 계산
    end_date = datetime.now()
    start_date = end_date - timedelta(days=2*365)  # 대략 2년을 일수로 계산

    # Yahoo Finance에서 주식 데이터 다운로드 (주어진 기간동안)
    stock = yf.Ticker(stock_symbol)
    data = stock.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

    # 필요한 데이터만 추출 (여기서는 'Open', 'High', 'Low', 'Close', 'Volume' 컬럼만)
    result = []
    for date, row in data.iterrows():
        result.append({
            "symbol": stock_symbol,
            "date": date.strftime('%Y-%m-%d'),
            "open": row['Open'],
            "high": row['High'],
            "low": row['Low'],
            "close": row['Close'],
            "volume": row['Volume']
        })

    return json.dumps(result)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        stock_symbol = sys.argv[1]
        stock_data = fetch_stock_data(stock_symbol)
        print(stock_data)
    else:
        print("주식 심볼을 입력하세요.")
