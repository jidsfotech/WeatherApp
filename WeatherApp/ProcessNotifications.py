#Process notification class for displaying popup status of current operation

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.properties import ObjectProperty
from kivy.clock import Clock
    

'''ProcessesIndicatorPopup, this class implents the Popup() class. the set_conn_error_msg method is used to dynamically set the various ecxeptions thrown when a user try to search for location and then display a popup of the error'''
class ProcessesIndicatorPopup(Popup):
    ProcesPopup = ObjectProperty()
    ecxept_trone = ObjectProperty()
    Progress_Bar = ProgressBar()
    
    #sets ecxeption errors trown on ProcessesIndicatorPopup conten label
    def set_conn_error_msg(self, ecxeptiontrone):
    
        if ecxeptiontrone == "ConnectionError":
            self.title = "No internet connection found"
            self.content = Label(text="could not connect to the internet")
            
        elif ecxeptiontrone == "Timeout":
            self.title = "Connection timed out"
            self.content = Label(text="Check device internet connection")
            
        elif ecxeptiontrone == "KeyError":
            self.title = "Location not found"
            self.content = Label(text="The location entered is not found")
            
        else:
            pass        


    def conn_indicator_popup(self):
        self.title = "connecting......"
        self.content = self.Progress_Bar.value = 1
        self.open()

    def calc_conn_progres(self):
        if self.Progress_Bar.value>=100:
            return False
            self.Progress_Bar.value += 1
            
    def conn_indicator_popup_on_open (self):
       Clock.schedule_interval(self.calc_conn_progres, 1/25)