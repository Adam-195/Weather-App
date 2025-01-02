import sys
import requests
import geocoder
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt
from cred import api_key #You may need to get your own API KEY from https://openweathermap.org/weather-conditions


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Today's Temps", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Search City", self)
        self.my_location = QPushButton("🧭 Use Current Location", self) # My Location Button
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.inputUI()

    def inputUI(self):
        self.setWindowTitle(f"Today's Temps")
        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.my_location) # My Location Button
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.my_location.setObjectName("my_location")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton{
                           font-family: Ageo Trial;
                           }
                           
                           QLabel#city_label{
                            font-size: 40px;
                            font-family: Ageo Trial Heavy;
                           }
                           
                           QLineEdit#city_input{
                            font-size: 38px;    
                           }
                           
                           QPushButton#my_location{
                            background-color: #ced1d7;
                            font-size: 15px;
                           }
                           
                           QPushButton#get_weather_button{
                            font-size: 25px;
                            background-color: #a9b5bd;
                           }
                          
                            QLabel#temperature_label{
                            font-size: 75px;
                            font-family: Poppins Black;

                           }
                           QLabel#emoji_label{
                            font-size: 120px;
                            font-family: Segoe UI Emoji;
                            }
                           
                           QLabel#description_label{
                            font-size: 22px;
                            font-family: Ageo Trial Thin;

                           }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)    
        self.my_location.clicked.connect(self.get_weather_location) 


    def get_weather(self):
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}" 

        try:
            reponse = requests.get(url)
            reponse.raise_for_status()
            data = reponse.json()
        
            if data["cod"] == 200:
                self.display_weather(data)
            
        except requests.exceptions.HTTPError:
            match reponse.status_code:
                case 400:
                 self.display_error("Bad Request:\nPlease Check City Name")
                case 401:
                 self.display_error("Unauthorised:\nInvalid API Key")
                case 403:
                 self.display_error("Access Denied:\nForbidden")
                case 404:
                 self.display_error("404 not found:\nPlease Check City Name")
                case 500:
                 self.display_error("Oops Internal Server Error:\nPlease Try Again Later")
                case 502:
                 self.display_error("Bad Gateway:\nInvalid Response from Server")
                case 503:
                 self.display_error(f"Service Unavaiable:\nCan't reach the server")
                case 504:
                 self.display_error("Timeout:\nNo Response from Server")
                case _:
                    self.display_error(f"HTTP Errorn:\n" + reponse.status_code)
               
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck Your Internet Connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe Request Timed out")    
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects:\nCheck URL")    
        except requests.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")    
            

    def get_weather_location(self):
        g = geocoder.ip('me')
        location = g.city
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"

        self.city_input.setText(location)

        try:
            reponse = requests.get(url)
            reponse.raise_for_status()
            data = reponse.json()
        
            if data["cod"] == 200:
                self.display_weather(data)
            
        except requests.exceptions.HTTPError:
            match reponse.status_code:
                case 400:
                 self.display_error("Bad Request:\nPlease Check City Name")
                case 401:
                 self.display_error("Unauthorised:\nInvalid API Key")
                case 403:
                 self.display_error("Access Denied:\nForbidden")
                case 404:
                 self.display_error("404 not found:\nPlease Check City Name")
                case 500:
                 self.display_error("Oops Internal Server Error:\nPlease Try Again Later")
                case 502:
                 self.display_error("Bad Gateway:\nInvalid Response from Server")
                case 503:
                 self.display_error(f"Service Unavaiable:\nCan't reach the server")
                case 504:
                 self.display_error("Timeout:\nNo Response from Server")
                case _:
                    self.display_error(f"HTTP Errorn:\n" + reponse.status_code)
               
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck Your Internet Connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe Request Timed out")    
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects:\nCheck URL")    
        except requests.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")    
            

    def display_error(self, message): 
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()

    def display_weather(self, data):
        temperature_k = data["main"]["temp"]
        temperature_c = round(temperature_k - 273.15)
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]
        

        self.temperature_label.setText(f"{temperature_c}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(f"{weather_description}")

    @staticmethod
    def get_weather_emoji(weather_id):
        if weather_id >=200 and weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "☁️"
        elif 500 <= weather_id <= 531:
            return "☔"
        elif 600 <= weather_id <= 622:
            return "☃️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif weather_id >= 801 and weather_id <= 804:
            return "☁️"
        else:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
