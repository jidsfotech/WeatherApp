# module containing fuctions for establishing search and requests
import json
import requests
from kivy.properties import  ListProperty
from requests.exceptions import ConnectionError, Timeout

#imports the ProcessesIndicatorPopup class from ProcessNotifications module 
from WeatherApp.ProcessNotifications import ProcessesIndicatorPopup 



#module-level function for establishing search intrsuction
#''''this method retrieves the location entred by the user, insert it in the openweather api url and then pass it to request() class to fetch the information which is then pass to json()class for decoding'''

def search(location, url_template):

        process_Indicator_popup = ProcessesIndicatorPopup()
        search_url = url_template.format(*location)
        
        try:
            #search for provided url and format the retuned data using json class into mor readable dict object 
            url_result = (requests.get(search_url)).text
            data = json.loads(url_result.decode()) if not isinstance(url_result, dict) else url_result
            return data
        #trow exceptions error when the occur and open   process_Indicator_popup 
        except ConnectionError:
            process_Indicator_popup.set_conn_error_msg("ConnectionError")
            
        except Timeout:
            process_Indicator_popup.set_conn_error_msg("Timeout")
        
        except KeyError: 
            process_Indicator_popup.set_conn_error_msg("KeyError")
            
        process_Indicator_popup.open()
        
        