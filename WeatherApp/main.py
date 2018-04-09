import kivy
import json
import requests

kivy.require('1.10.0')

from kivy import Config
Config.set('graphics', 'multisamples', '0')
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton
from kivy.uix.button import Button
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty,StringProperty, ListProperty, NumericProperty
#imports the ProcessesIndicatorPopup class from ProcessNotifications module 
from WeatherApp.ProcessNotifications import ProcessesIndicatorPopup 
#improt search function from IniciateRequest module 
from WeatherApp.IniciateRequest import search



#implents the ListItemButton added to listview class
class LocationButton(ListItemButton):
    location = ListProperty()

#class for displaing current wearther condition  of searched locations
class CurrentWeatherForm(BoxLayout):
    location = ListProperty(['New York', 'US'])
    conditions = StringProperty()
    temp = NumericProperty()
    temp_min = NumericProperty()
    temp_max = NumericProperty()
    
    #retrieve avd updates weather information for the selected location 
    def Retrieve_Update_Weather(self):
        search_template = "http://api.openweathermap.org/data/2.5/" + "weather?q={},{}&units=metrics" + "&APPID=46dc006c130ecf6e18c0d33dffbd39da"
        get_weather_data = search(self.location, search_template)
        data = get_weather_data   
        if data:        
            self.conditions = data['weather'][0]['description']
            self.temp = data['main']['temp']
            self.temp_min = data['main']['temp_min']
            self.temp_max = data['main']['temp_max']  
        
               
#Weatherapp root widget        
class WeatherRoot(BoxLayout):
    addlocation = ObjectProperty()
    current_weather = ObjectProperty()
        
    # called by locationbutton, which sets the location property variable with users selction. 
    def show_current_weather(self,  location=None):
        self.clear_widgets()
       
        if self.current_weather is None:
            #creates object of the CurrentWeatherForm and set the location property variable of the class object
            self.current_weather = CurrentWeatherForm()
            
        if location is not None:
            self.current_weather.location = location
            
        #call CurrentWeatherForm Retrieve_Update_Weather
        self.current_weather.Retrieve_Update_Weather()
        self.add_widget(self.current_weather)
    
    #create object of the AddLocationForm 
    def show_addLocationForm(self):
        self.clear_widgets()
        adlocationform = AddLocationForm()
        adlocationform.canclebutton.height = "30dp"
        adlocationform.canclebutton.text = "Cancle"
        addlocation = self.add_widget(adlocationform)
        return addlocation
    
#AddLocationForm for adding location to search for 
class AddLocationForm(BoxLayout):
    search_input = ObjectProperty()
    
    #search and update listview data object with search result 
    def search_location(self):
        '''this method retrieves the location entred by the user, insert it in the openweather api url and then pass it to request() class to fetch the information which is then pass to json()class for decoding'''
    
        search_template = "http://api.openweathermap.org/data/2.5/"+"find?q={}&type=like"+"&APPID=46dc006c130ecf6e18c0d33dffbd39da"
        
        #implents the search function module and search  user input 
        search_location_data = search((self.search_input.text,), search_template)
        data = search_location_data
        if data:
            cities = [(d["name"], d["sys"]["country"]) for d in data['list']]
            print (cities)
            self.search_results.adapter.data[:]
            self.search_results.adapter.data.extend(cities)
            self.search_results._reset_spopulate()
        
                    
    #set location property on the button with tuple of search location 
    def args_converter(self, index, data_item):
        city,country = data_item
        return {'location': (city,country)}

#weather app mian app class         
class WeatherApp(App):
    pass

if __name__ == '__main__':
    WeatherApp().run()




