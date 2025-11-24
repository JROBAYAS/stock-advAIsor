#!/usr/bin/env python3
"""
Script para ejecutar main.py en local cargando credenciales desde credentials.yaml
"""
import os
import sys
import yaml
from pathlib import Path

def load_credentials():
    """Carga las credenciales desde el archivo credentials.yaml"""
    credentials_path = Path(__file__).parent / "credentials.yaml"
    
    if not credentials_path.exists():
        print(f"❌ Error: No se encontró el archivo {credentials_path}")
        sys.exit(1)
    
    with open(credentials_path, 'r', encoding='utf-8') as f:
        credentials = yaml.safe_load(f)
    
    return credentials

def set_environment_variables(credentials):
    """Configura las variables de entorno necesarias"""
    # Configurar email
    email_config = credentials.get('email_notifications', {})
    os.environ['EMAIL_USER'] = email_config.get('email', '')
    os.environ['EMAIL_PWD'] = email_config.get('pwd_app', '')
    # os.environ['OPENAI_API_KEY'] = credentials.get('openai', {}).get('api_key', '')
    os.environ['NEWSAPI_API_KEY'] = credentials.get('newsapi', {}).get('api_key', '')
    os.environ['GROQ_API_KEY'] = credentials.get('grog', {}).get('api_key', '')
    
    # Configurar otras variables si es necesario
    settings = credentials.get('settings', {})
    os.environ['ENVIRONMENT'] = settings.get('environment', 'development')
    os.environ['DEBUG'] = str(settings.get('debug', True))
    
    print("✓ Variables de entorno configuradas:")
    print(f"  - EMAIL_USER: {os.environ['EMAIL_USER']}")
    print(f"  - ENVIRONMENT: {os.environ['ENVIRONMENT']}")
    print(f"  - DEBUG: {os.environ['DEBUG']}")
    print()


if __name__ == "__main__":
    # Cargar credenciales
    print("📁 Cargando credenciales desde credentials.yaml...")
    credentials = load_credentials()

     # Configurar variables de entorno
    set_environment_variables(credentials)
    
    # Importar y ejecutar main
    print("▶️  Ejecutando main.py...")
    print("-" * 60)
    
    try:
        from main import main
        main()
        print("✅ Ejecución completada exitosamente")
            
    except Exception as e:
        print("-" * 60)
        print(f"❌ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

