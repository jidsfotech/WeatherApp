import kivy
import json
import requests

kivy.require('1.10.0')

from kivy import Config
Config.set('graphics', 'multisamples', '0')
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label 
from kivy.uix.button import Button 
from kivy.properties import ObjectProperty,StringProperty, ListProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.storage.jsonstore import JsonStore

#improt search function from IniciateRequest module 
from WeatherApp.IniciateRequest import search

# this is the location button for responding to user selection
#implents the RecycleDataViewBehavior and Button  uses as the RecycleView class vieew class 
class LocationButton(RecycleDataViewBehavior, Button):
    location = ListProperty()
    index = None
    
    # """ Add selection support to the Label """
    def refresh_view_attrs(self, rv, index, data):
        """Catch and handle the view changes"""
        self.index = index
        return super(LocationButton, self).refresh_view_attrs(rv, index, data)
    

#show current location screen for displaying waether fo selected location
class CurrentWeatherForm(Screen):
    location = ListProperty(['New York', 'US'])
    conditions = StringProperty()
    temp = NumericProperty()
    temp_min = NumericProperty()
    temp_max = NumericProperty()
    
    #retrieve avd updates weather information for the selected location 
    def Retrieve_Update_Weather(self):
        weather_template = "http://api.openweathermap.org/data/2.5/" + "weather?q={},{}&units=metrics" + "&APPID=46dc006c130ecf6e18c0d33dffbd39da"
        get_weather_data = search(self.location, search_template)
        data = get_weather_data
        if data:
            self.conditions = data['weather'][0]['description']
            self.temp = data['main']['temp']
            self.temp_min = data['main']['temp_min']
            self.temp_max = data['main']['temp_max']

class Error_Msg_Popup(Popup):

    '''Popup modal window, this class implents the Popup() class. the Error_Msg method is used to dynamically set and display the various ecxeptions thrown when a user try to search for location'''
    
    def Error_Msg(self, title="", size=(), Err=""):
        self.title = title
        self.size = size
        self.content = Label(text=Err)  
        
#Weatherapp root widget   
#add location screen this is the main screen     
class WeatherRoot(ScreenManager):
    addlocation = ObjectProperty()
    current_weather = ObjectProperty()
    
    # called by locationbutton, which sets the location property variable with users selct
    def show_current_weather(self, location=None):
        self.clear_widgets()

        if self.current_weather is None:
            #creates object of the CurrentWeatherForm and set the location property variable of the class object
            self.current_weather = CurrentWeatherForm()

        if location is not None:
            self.current_weather.location = location
            
        #call CurrentWeatherForm Retrieve_Update_Weather
        self.current_weather.Retrieve_Update_Weather()
        self.add_widget(self.current_weather)
        self.current = "CurrentWeatherForm"
        
    #create object of the AddLocationForm    
    def show_addLocationForm(self):
        self.clear_widgets()
        adlocationform = AddLocationForm()
        adlocationform.canclebutton.height = "30dp"
        adlocationform.canclebutton.text = "Cancle"
        addlocation = self.add_widget(adlocationform)
        self.current = "AddLocationForm"
        
class AddLocationForm(Screen):
    def search_location(self):
    
        search_template = "http://api.openweathermap.org/data/2.5/"+"find?q={}&type=like"+"&APPID=46dc006c130ecf6e18c0d33dffbd39da"
        
        #implents the search function module and search  user input 
        search_location_data = search((self.ids.CityToSearch.text,), search_template)
        data = search_location_data
        if data: 
            cities = [{'text':"{} ({})".format(d["name"], d["sys"]["country"])} for d in data['list']]
            self.search_results.data = cities
           
        
        '''Wdata = JsonStore('weatherdata.json')
        cities = [{"location":(d["name"], d["sys"]["country"])} for d in Wdata['list']]
        del self.search_results.data[:]
        self.search_results.data = cities'''





#weather app mian app class 
class WeatherApp(App):
    pass

if __name__ == '__main__':
    WeatherApp().run()