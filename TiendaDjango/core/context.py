import requests
import urllib3

# ★ Opcional: silencia la advertencia de certificado inseguro
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def daily_quote(request):
    """
    Llama a https://api.quotable.io para traer una cita aleatoria,
    ignora la validación SSL (certificado expirado) y devuelve
    en el contexto un dict bajo la clave 'daily_quote' con dos campos:
      - text
      - author
    """
    quote = {}
    try:
        r = requests.get(
            "https://api.quotable.io/random?maxLength=100",
            timeout=2,
            verify=False           # <— igual que curl -k
        )
        r.raise_for_status()
        data = r.json()
        quote = {
            'text':   data.get('content', ''),
            'author': data.get('author',  '')
        }
    except Exception:
        quote = {}
    return { 'daily_quote': quote }
