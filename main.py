import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

import yfinance as yf
import requests
from src.fetch_news import fetch_company_news
from src.fetch_prices import fetch_stock_summary
from src.sum_llm import fetch_company_news_llm, summarize_stock_report, get_list_tickers_most_mentioned_and_important_in_news


EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PWD = os.getenv("EMAIL_PWD")

DATE_TODAY = (datetime.now() - timedelta(days=0)).strftime("%Y-%m-%d")  # Usar día anterior para datos completos


def send_email(msg_content):
    msg = MIMEText(msg_content)
    msg["Subject"] = "Hello World - Ejecución automática"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_USER  # puedes enviar a ti mismo

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PWD)
        server.send_message(msg)


def build_report(tickers):
    '''
    Construye el reporte diario de mercado para los tickers dados.
    
    Args:
        tickers (dict): Diccionario con símbolos de ticker como claves y nombres de empresa como valores.
    
    Returns:
        str: Reporte formateado como texto.
    
    
    tickers = {
            "AAPL": "Apple",
            "MSFT": "Microsoft",
            "AMZN": "Amazon",
        }
    '''
    report = "📊 Reporte Diario de Mercado\n\n"

    if tickers is None:
        tickers = get_list_tickers_most_mentioned_and_important_in_news(DATE_TODAY, top_n=10)

    for ticker, name in tickers.items():
        print(ticker, name)
        info = fetch_stock_summary(ticker)
        print(f"Precio para {ticker}: {info['price']} USD, Cambio: {info['change']}%")
        
        # news = fetch_company_news(ticker, name)
        # print(f"Noticias para {ticker}: {len(news)} artículos")
        # news_str = "\n".join([f"- {n['title']}" for n in news])
        news_str = fetch_company_news_llm(ticker, name, DATE_TODAY)
        # print(news_str)
    
        summary = summarize_stock_report(ticker, news_str, info)

        report += f"### {name} ({ticker}) ###\n"
        report += summary + "\n\n"

    return report


def main(TICKERS=None):
    """Función principal"""
    print("=" * 60)
    print("🚀 Ejecutando main.py en modo local")
    print("=" * 60)
    print()

    report = build_report(TICKERS)
    # print(report)
    
    send_email(report)


if __name__ == "__main__":
    main()
