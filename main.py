import requests
import pandas as pd
import np
from bs4 import BeautifulSoup
import customtkinter
import csv
import tkinter


# Function to scrape the data from the website
def scrape_url():
        url = 'https://www.engineeringtoolbox.com/engineering-materials-properties-d_1225.html'
        html = requests.get(url).content
        df_list = pd.read_html(html)
        with open('Material properties.csv','a') as f:
              for df in df_list:
                   df.to_csv(f)
                   f.write("\n")

# Function to verify if the material is suitable for the given stress and mass
def check_material():
        M = float(entry1.get())
        T = float(entry2.get())
        Max_shear = str(np.sqrt((M/2)**2 + T**2))
        Von_Mises = str(np.sqrt(M**2 + 3*T**2))
        Max_shear_allowed = []
        Von_Mises_allowed = []
        df = pd.read_csv('Material properties.csv', on_bad_lines='skip',encoding='unicode_escape')
        df.columns = (['0','Material', 'Density', 'Tensile Modulus', 'Tensile Strength', 'Specific Modulus','Specific Strength','Maximum Service Temperature'])
        df = df.drop(columns=['Maximum Service Temperature'])
        yield_strength = df['Tensile Strength']
        V = int(entry3.get())
        allowed_m = int(entry4.get())
        df = df[df['Density']<str(allowed_m/V)]
        for value in yield_strength:
            if value > Von_Mises:
                Von_Mises_allowed.append(df["Material"])
            else:
                pass
        for value in yield_strength:
            if value > Max_shear:
                Max_shear_allowed.append(df["Material"])
            else:
                pass
        Allowed_materials = {'Max_shear_allowed': Max_shear_allowed, 'Von_Mises_allowed': Von_Mises_allowed}
        print(Allowed_materials)
         
# App GUI
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Web Scraper")

title = customtkinter.CTkLabel(app, text = "Normal Stress (MPa)", font = ("Arial", 12))
title.pack(padx=10, pady=10)

entry1 = customtkinter.CTkEntry(app, width = 40, height = 40)
entry1.pack()

title = customtkinter.CTkLabel(app, text = "Shear Stress (MPa)", font = ("Arial", 12))
title.pack(padx=10, pady=10)

entry2 = customtkinter.CTkEntry(app, width = 40, height = 40)
entry2.pack()

title = customtkinter.CTkLabel(app, text = "Volume (m^3)", font = ("Arial", 12))
title.pack(padx=10, pady=10)

entry3 = customtkinter.CTkEntry(app, width = 40, height = 40)
entry3.pack()

title = customtkinter.CTkLabel(app, text = "Allowed mass (kg)", font = ("Arial", 12))
title.pack(padx=10, pady=10)

entry4 = customtkinter.CTkEntry(app, width = 40, height = 40)
entry4.pack()

Calculate = customtkinter.CTkButton(app, text = "Calculate", command = check_material)
Calculate.pack(padx=10, pady=10)

app.mainloop()