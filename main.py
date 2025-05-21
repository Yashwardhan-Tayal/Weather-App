from tkinter import *
import requests
import os
from PIL import Image, ImageTk
from io import BytesIO
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv('API_KEY')
def click():
    city=e.get()
    url=f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    errortext='error occurred:'
    try:
        response=requests.get(url)
        data=response.json()
        response.raise_for_status()
        temp=str(data['main']['temp'])+'°'
        weather=data['weather'][0]['main']
        desc=data['weather'][0]['description']
        iconcode=data['weather'][0]['icon']
        iconurl=f'https://openweathermap.org/img/wn/{iconcode}@4x.png'
        iconreq=requests.get(iconurl)
        iconimg=Image.open(BytesIO(iconreq.content))
        icon=ImageTk.PhotoImage(iconimg)
        output=Label(text=("\n"+str(temp)+"\n\n"+desc),
                font=('Arial',40),
                bg='#87CEEB',
                width=600,
                image=icon,
                compound='bottom')
        output.image=icon
        output.grid(row=3,column=0)
    except requests.exceptions.HTTPError as http_error:
        match response.status_code:
            case 400:
                errortext="Bad request:\nPlease check your input"
            case 401:
                errortext="Unauthorized:\nInvalid API key"
            case 403:
                errortext="Forbidden:\nAccess is denied"
            case 404:
                errortext="Not found:\nCity not found"
            case 500:
                errortext="Internal Server Error:\nPlease try again later"
            case 502:
                errortext="Bad Gateway:\nInvalid response from the server"
            case 503:
                errortext="Service Unavailable:\nServer is down"
            case 504:
                errortext="Gateway Timeout:\nNo response from the server"
            case _:
                errortext=f"HTTP error occurred:\n{http_error}"
        errorlabel=Label(text=errortext,
                        width=50,
                        height=12,
                        bg='#87CEEB',
                        font=(None,20)).grid(row=3,column=0)
    except requests.exceptions.ConnectionError:
        errortext="Connection Error:\nCheck your internet connection"
        errorlabel=Label(text='Error',
                        width=50,
                        height=12,
                        bg='#87CEEB',
                        font=(None,20)).grid(row=3,column=0)
    except requests.exceptions.Timeout:
        errortext="Timeout Error:\nThe request timed out"
        errorlabel=Label(text='Error',
                        width=50,
                        height=12,
                        bg='#87CEEB',
                        font=(None,20)).grid(row=3,column=0)
    except requests.exceptions.TooManyRedirects:
        errortext="Too many Redirects:\nCheck the URL"
        errorlabel=Label(text='Error',
                        width=50,
                        height=12,
                        bg='#87CEEB',
                        font=(None,20)).grid(row=3,column=0)
    except requests.exceptions.RequestException as req_error:
        errortext=f"Request Error:\n{req_error}"
        errorlabel=Label(text='Error',
                        width=50,
                        height=12,
                        bg='#87CEEB',
                        font=(None,20)).grid(row=3,column=0)

w=Tk()
w.title("Weather App")
w.configure(bg='#87CEEB')
introlabel=Label(text="Enter the city name:",
                 font=('Arial',15),
                 bg='#87CEEB').grid(row=0,column=0)
b=Button(w,
         text='Get Weather',
         command=click,
         fg='black',
         bg='white',
         font=(None,20,'bold'),
         activeforeground='black',
         activebackground='white')
e=Entry(w,
        font=('Arial',50),
        width=15)
e.grid(row=1,column=0)
b.grid(row=2,column=0)
t=Label()
w=Label()
w.mainloop()