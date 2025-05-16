import requests

def daily_quote(request):
    quote = {}
    try:
        r = requests.get("https://api.quotable.io/random?maxLength=100", timeout=2)
        r.raise_for_status()
        data = r.json()
        quote = {
            'text':   data.get('content',''),
            'author': data.get('author','')
        }
    except:
        quote = {}
    return {'daily_quote': quote}
