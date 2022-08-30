from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
class Crypto:
    def get_top_5(self):

        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
      
        parameters = {
          'start':'1',
          'limit':'1000',
          'convert':'USD'
        }
        headers = {
          'Accepts': 'application/json',
          'X-CMC_PRO_API_KEY': 'e78f3b56-f020-4b5f-8831-cbfc68ea37ec',
        }

        session = Session()
        session.headers.update(headers)

        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data['data']

    
