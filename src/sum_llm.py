import os
from openai import OpenAI
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("🔑 Inicializando cliente OpenAI...")
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_stock_report(ticker, news, price_info):
    prompt = f"""
    Resume brevemente para un reporte financiero:
    Activo: {ticker}
    Precio actual: {price_info["price"]}
    Cambio diario: {price_info["change"]}%
    Noticias recientes:
    {news}
    
    Incluye:
    - Riesgos a corto plazo
    - Oportunidades
    - Breve recomendación (comprar/mantener/vender)

    Modelos recomendados:
    llama-3.1-70b-versatile (muy bueno)
            model="llama3-70b-8192", deprecated
    mixtral-8x7b (muy bueno en resumen)
    """
    if os.getenv("GROQ_API_KEY"):
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
    else:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
    
    return response.choices[0].message.content

   
