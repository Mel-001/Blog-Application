import requests


base_url = None
def configure_request(app):
    global base_url
    base_url = app.config['API_URL']
def get_quotes():
    """
    Function that gets the json response to our url request
    """
    get_response = requests.get('http://quotes.stormconsultancy.co.uk/random.json').json()
    return get_response