import os
import smtplib
from email.mime.text import MIMEText

import yfinance as yf
import requests
from src.fetch_news import fetch_company_news
from src.fetch_prices import fetch_stock_summary
from src.sum_llm import summarize_stock_report


EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PWD = os.getenv("EMAIL_PWD")

def send_email(msg_content):
    msg = MIMEText(msg_content)
    msg["Subject"] = "Hello World - Ejecución automática"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_USER  # puedes enviar a ti mismo

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PWD)
        server.send_message(msg)


def build_report(tickers):
    report = "📊 Reporte Diario de Mercado\n\n"

    for ticker, name in tickers.items():
        info = fetch_stock_summary(ticker)
        news = fetch_company_news(ticker, name)
        news_str = "\n".join([f"- {n['title']}" for n in news])

        summary = summarize_stock_report(ticker, news_str, info)

        report += f"### {name} ({ticker}) ###\n"
        report += summary + "\n\n"

    return report


def main():
    """Función principal"""
    print("=" * 60)
    print("🚀 Ejecutando main.py en modo local")
    print("=" * 60)
    print()
    TICKERS = {
        "NVDA": "NVIDIA",
        "TSLA": "Tesla",
        "GOOGL": "Google",
    }

    report = build_report(TICKERS)
    send_email(report)


if __name__ == "__main__":
    main()
