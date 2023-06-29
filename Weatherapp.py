from tkinter import *
from tkinter import ttk
import requests
from tkinter import simpledialog
import easygui
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys
from dotenv import load_dotenv
import os
load_dotenv()
if os.getenv("API_KEY") == "weatherapi_key":
    easygui.msgbox("No api key found, Did you enter the api key correctly?")
else: 
    sys.setrecursionlimit(10000)
    def close_loading():
        root.destroy()
    def get_ip_address():
                url = 'https://api.ipify.org'
                response = requests.get(url)
                ip_address = response.text
                return ip_address
    root = tk.Tk()
    root.title("Loading Page")
    root.geometry("750x300")
    root.resizable(False, False)
    ip = get_ip_address() #to reduce wait time i already call the function here
    loading_label = ttk.Label(root, text="Loading...", font=("Arial", 14))
    loading_label.pack(pady=50)
    progress_bar = ttk.Progressbar(root, length=700, mode='indeterminate')
    progress_bar.pack()
    root.after(500, close_loading)
    progress_bar.start(3)

    root.mainloop()
    def get_location():
        if entry.get()=="":
            location.append(ip)
            win.destroy()
        else:
            location.append(entry.get())
            win.destroy()

    location = []

    win = Tk()
    win.resizable(False, False)
    win.geometry("750x300")
    win.iconphoto(False, PhotoImage(file='logo.png'))
    win.title("Location")

    label = Label(win, text="Enter Location \nPass US Zipcode, UK Postcode, Canada Postalcode, IP address, \nLatitude/Longitude (decimal degree) or city name.\nUse Latitude/Longitude for a guaranteed result.")
    label.pack()

    entry = Entry(win, width=40)
    entry.pack()

    ttk.Button(win, text="Okay", width=20, command=get_location).pack(pady=20)

    win.mainloop()


    url = "http://api.weatherapi.com/v1/current.json?key="+os.getenv('API_KEY')+"&q="+location[0]+"&aqi=no"
    url2 = "http://api.weatherapi.com/v1/forecast.json?days=14&key="+os.getenv('API_KEY')+"&q="+location[0]
    url3 = "http://api.weatherapi.com/v1/forecast.json?alerts=yes&key="+os.getenv('API_KEY')+"&q="+location[0]
    getweather = requests.post(url) #get data from api
    weathernextweek = requests.post(url2)
    alertslist = requests.post(url3)
    data = getweather.json()
    data2 = weathernextweek.json()
    data3 = alertslist.json()
    loc1 = data['location']['country']
    loc2 = data['location']['name']
    loc3 = data['location']['region']
    locfull = loc1+",\n"+loc2+",\n"+loc3
    date_list = [] #lists for graphs
    max_temperature_list = []
    min_temperature_list = []
    rain_probability_list = []
    temphour_list = []
    for day in range (0, 14): # get data
        try:
            day_date = data2['forecast'] ['forecastday'] [day]['date']
            day_maxtemp = data2['forecast']['forecastday'][day]['day']['maxtemp_c']
            day_mintemp = data2['forecast']['forecastday'][day]['day']['mintemp_c']
            day_rainchance = data2['forecast']['forecastday'][day]['day']['daily_chance_of_rain']
            refresh = data['current']['last_updated']

            rounded_max_temp = round(day_maxtemp)
            rounded_min_temp = round(day_mintemp)
            rounded_rainchanche = round(day_rainchance)
            day_mmdd = day_date.replace("2023-", "")
            date_list.append(day_mmdd) # append data to lists
            max_temperature_list.append(int(rounded_max_temp))
            rain_probability_list.append(int(rounded_rainchanche))
            min_temperature_list.append(int(rounded_min_temp))
        except:
            print("Error")
    root = Tk(screenName="Weather")
    root.title("Weather app")
    root.resizable(False, False)
    root.iconphoto(False, tk.PhotoImage(file='logo.png'))

    frm = ttk.Frame(root, padding=20)
    frm.grid()
    ttk.Label(frm, text="What do you want to know").grid(column=0, row=0)
    ttk.Label(frm, text="Location\n"+locfull+"\n\n\nMade by Wsk Fl").grid(column=0, row=3)

    def quit():
        quit()

    def Temp():
        root = tk.Tk()
        root.title("Temparature")
        root.resizable(False, False)

        date = date_list
        percentages = max_temperature_list
        percentages2 = min_temperature_list

        fig = Figure(figsize=(16, 4), dpi=100)

        ax = fig.add_subplot(111)
        ax.bar(date, percentages, width=0.4, color='red', label='Max')
        ax.bar(date, percentages2, width=0.4, color='blue', label='Min')
        ax.legend()
        ax.set_title('Temperature')
        ax.set_xlabel('Date')
        ax.set_ylabel('Temperature (°C)')

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack()

        print("Last refresh " + refresh)

    def Rain():
        root = tk.Tk()
        root.title("Rain probability")
        root.resizable(False, False)

        fig = Figure(figsize=(16, 4), dpi=100)
        ax = fig.add_subplot(111)

        date = date_list
        percentages = rain_probability_list

        ax.bar(date, percentages, width=0.4, color='blue')
        ax.set_title('Rain probability')
        ax.set_xlabel('Date')
        ax.set_ylabel('Percentage')

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def TempHour():
        day = simpledialog.askstring(title="Date",
                                    prompt="      What Date? (yyyy-mm-dd)(or leave blank for todays date)      ")
        
        root = tk.Tk()
        root.resizable(False, False)
        root.title("Temprature per hour")
        fig = Figure(figsize=(16, 4), dpi=100)

        ax2 = fig.add_subplot()
        ax2.set_title('Temperature per hour')
        ax2.set_xlabel('Hour')
        ax2.set_ylabel('Temperature (°C)')

        tick_positions = np.arange(0, 24)
        tick_labels = np.arange(0, 24)

        ax2.set_xticks(tick_positions)
        ax2.set_xticklabels(tick_labels)    

        try:
            if day in date_list:
                dayindex = date_list.index(day)
        except ValueError:
            pass
        print("no Input")
        try:
            for i in range(0, 24):
                    dayindex = date_list.index(day)
                    hourtemp = data2['forecast']['forecastday'][dayindex]["hour"][i]["temp_c"]
                    temphour_list.append(int(hourtemp))

                    ax2.bar(i, hourtemp, width=0.4, color='red')

        except ValueError:
            for i in range(0, 24):
                    hourtemp = data2['forecast']['forecastday'][0]["hour"][i]["temp_c"]
                    temphour_list.append(int(hourtemp))

                    ax2.bar(i, hourtemp, width=0.4, color='red')

        else:
                print("Error in temphour but you can ignore it")
        
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack()
        
    def Alerts():
            for o in range(0, 999):
                try:
                    print(o)
                    alert_title = data3['alerts']['alert'][o]['headline'] #get data from json
                    alert_event = data3['alerts']['alert'][o]['event']
                    alert_effective = data3['alerts']['alert'][o]['effective']
                    alert_expires = data3['alerts']['alert'][o]['expires']
                    alert_desc = data3['alerts']['alert'][o]['desc']

                    easygui.msgbox("Alert from: " + alert_title + " \n Type: " + alert_event + " \n Description " + alert_desc + " \n from " + alert_effective + " until " + alert_expires, title="Weather Alert")
                
                except:
                    print("No alerts left")
                    easygui.msgbox("No Alerts Left")     

                    break

    ttk.Button(frm, text="Temperatur", command=Temp).grid(column=10, row=0)
    ttk.Button(frm, text="Rain Probability", command=Rain).grid(column=10, row=1)
    ttk.Button(frm, text="Temperatur by the hour", command=TempHour).grid(column=10, row=2)
    ttk.Button(frm, text="Current alerts", command=Alerts).grid(column=10, row=3)
    ttk.Button(frm, text="Quit", command=quit).grid(column=10, row=4)

    root.mainloop()
