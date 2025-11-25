import os
import json
from openai import OpenAI
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("🔑 Inicializando cliente OpenAI...")
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_stock_report(ticker, news, price_info):
    '''
    Resume un reporte financiero para un activo dado usando un modelo LLM.
    
    Args:
        ticker (str): Símbolo del activo.
        news (str): Noticias recientes relacionadas con el activo.
        price_info (dict): Información de precios con claves "price" y "change".
    
    Modelos recomendados:
    llama-3.1-70b-versatile (muy bueno)
            model="llama3-70b-8192", deprecated
    mixtral-8x7b (muy bueno en resumen)
    '''
    prompt = f"""
    Resume brevemente para un reporte financiero:
    Activo: {ticker}
    Precio actual: {price_info["price"]}
    Cambio diario: {price_info["change"]}%
    Noticias recientes:
    {news}
    
    Incluye:
    - Riesgos a corto plazo con noticia de ultima hora
    - Breve recomendación (comprar/mantener/vender) segun cambios de ultimos dias y ultimas semanas
    
    -> No más de 150 palabras
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

   
def get_list_tickers_most_mentioned_and_important_in_news(date:str, top_n:int=10)->dict:
    """
    Obtiene un diccionario de los tickers más mencionados e importantes en las noticias financieras del día dado.
    
    Args:
        date (str): Fecha en formato 'YYYY-MM-DD'.
        top_n (int): Número de tickers a retornar.
    
    Returns:
        dict: Diccionario con símbolos de ticker como claves y nombres de empresas como valores.
              Ejemplo: {'AAPL': 'Apple', 'MSFT': 'Microsoft'}
    """
    prompt = f"""
    Proporciona una lista de los {top_n} tickers más mencionados e 
    importantes en las noticias financieras del día {date} y 2 dias mas atras, en ese rango lo mas destacado.
    
    Devuelve la respuesta ÚNICAMENTE en formato JSON con la siguiente estructura:
    {{
        "TICKER1": "Nombre de la Empresa 1",
        "TICKER2": "Nombre de la Empresa 2"
    }}
    
    Ejemplo:
    {{
        "AAPL": "Apple",
        "MSFT": "Microsoft",
        "GOOGL": "Alphabet",
        "TSLA": "Tesla"
    }}
    
    No incluyas explicaciones adicionales, solo el JSON.
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
    
    tickers_str = response.choices[0].message.content
    
    # Extraer el JSON del contenido (por si viene con markdown code blocks)
    if "```json" in tickers_str:
        tickers_str = tickers_str.split("```json")[1].split("```")[0].strip()
    elif "```" in tickers_str:
        tickers_str = tickers_str.split("```")[1].split("```")[0].strip()
    
    try:
        tickers_dict = json.loads(tickers_str)
        return tickers_dict
    except json.JSONDecodeError as e:
        print(f"Error al parsear JSON: {e}")
        print(f"Respuesta recibida: {tickers_str}")
        return {}
    

def fetch_company_news_llm(ticker, company_name, date):
    """
    ticker: str, ejemplo 'AAPL'
    company_name: str, ejemplo 'Apple'
    """
    prompt = f"""
    Proporciona un resumen breve de las noticias más relevantes para la empresa {company_name} ({ticker}).
    Limita el resumen a 5 puntos clave.
    para el dia de {date} y los 1 dias anteriores.
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



