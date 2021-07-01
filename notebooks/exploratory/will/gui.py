# Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from scipy.stats import zscore
from scipy import stats
from tkinter import *
from PIL import Image, ImageTk
import pickle
from collections import Counter
import warnings
warnings.filterwarnings("ignore")


with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("ohe.pkl", "rb") as f:
    ohe = pickle.load(f)\

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
    
def is_number(a):
    # will be True also for 'NaN'
    try:
        number = float(a) or number == int(a)
        return True
    except ValueError:
        return False

def clean(df):
    df['sqft_living'] = df['sqft_living'].astype(float)
    df['bedrooms'] = df['bedrooms'].astype(float)
    df['bathrooms'] = df['bathrooms'].astype(float)
    df['grade'] = df['grade'].astype(float)
    df['sqft_above'] = df['sqft_above'].astype(float)
    df['sqft_living15'] = df['sqft_living15'].astype(float)
    df['sqft_lot15'] = df['sqft_lot15'].astype(float)
    df['sqft_lot'] = df['sqft_lot'].astype(float)
    df['floors'] = df['floors'].astype(float)
    df["yr_built"] = df["yr_built"].astype(float)
    df['zipcode'] = df['zipcode'].astype(int)
    
    df["age"] = df["yr_built"].map(lambda x: 2021 - x)
    df["months_ago_sold"] = df["date"].map(lambda date: float(date.split("/")[0]) + (2021- float(date.split("/")[2]))*12)
    
    # Top cross correlations via function at head of notebook
    df["sqft_living&above"] = df["sqft_living"] * df["sqft_above"]
    df["sqft_living&grade"] = df["sqft_living"] * df["grade"]
    df["sqft_living&living15"] = df["sqft_living"] * df["sqft_living15"]
    df["grade&sqft_above"] = df["grade"] * df["sqft_living"]
    df["bathrooms&sqft_living"] = df["bathrooms"] * df["sqft_living"]
    df["sqft_above&sqft_living15"] = df["sqft_above"] *df["sqft_living15"]
    df["grade&sqft_above"] = df["grade"] * df["sqft_above"]
    df["grade&sqft_living15"] = df["grade"] * df["sqft_living15"]
    df["grade&sqft_above"] = df["grade"] * df["sqft_above"]
  

    onehot_data = ohe.transform(df[['zipcode']])
    zip_code = pd.DataFrame(onehot_data, columns=ohe.get_feature_names())
    df = pd.concat([df, zip_code],axis=1)

    df.drop(['yr_built', 'date', 'zipcode'], axis=1, inplace=True)
    #drop outliers
    
    return df

# Gather data from user via GUI

# Format data (convert data types, create new columns, scale, ohe)

# Make prediction

def get_prediction(features):
    features = features[['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'grade',
       'sqft_above', 'sqft_living15', 'sqft_lot15', 'age', 'months_ago_sold',
       'x0_98001.0', 'x0_98002.0', 'x0_98003.0', 'x0_98004.0', 'x0_98005.0',
       'x0_98006.0', 'x0_98007.0', 'x0_98008.0', 'x0_98010.0', 'x0_98011.0',
       'x0_98014.0', 'x0_98019.0', 'x0_98022.0', 'x0_98023.0', 'x0_98024.0',
       'x0_98027.0', 'x0_98028.0', 'x0_98029.0', 'x0_98030.0', 'x0_98031.0',
       'x0_98032.0', 'x0_98033.0', 'x0_98034.0', 'x0_98038.0', 'x0_98039.0',
       'x0_98040.0', 'x0_98042.0', 'x0_98045.0', 'x0_98052.0', 'x0_98053.0',
       'x0_98055.0', 'x0_98056.0', 'x0_98058.0', 'x0_98059.0', 'x0_98065.0',
       'x0_98070.0', 'x0_98072.0', 'x0_98074.0', 'x0_98075.0', 'x0_98077.0',
       'x0_98092.0', 'x0_98102.0', 'x0_98103.0', 'x0_98105.0', 'x0_98106.0',
       'x0_98107.0', 'x0_98108.0', 'x0_98109.0', 'x0_98112.0', 'x0_98115.0',
       'x0_98116.0', 'x0_98117.0', 'x0_98118.0', 'x0_98119.0', 'x0_98122.0',
       'x0_98125.0', 'x0_98126.0', 'x0_98133.0', 'x0_98136.0', 'x0_98144.0',
       'x0_98146.0', 'x0_98148.0', 'x0_98155.0', 'x0_98166.0', 'x0_98168.0',
       'x0_98177.0', 'x0_98178.0', 'x0_98188.0', 'x0_98198.0', 'x0_98199.0',
       'sqft_living&above', 'sqft_living&grade', 'sqft_living&living15',
       'grade&sqft_above', 'bathrooms&sqft_living', 'sqft_above&sqft_living15',
       'grade&sqft_living15']]
    
    print('Feature columns: ', features.columns)

    #get prediction
    pred = model.predict(features)
    
    #reverse log
    #pred = np.exp(pred)
    return pred

def click():
    entries = []
    column_names = ["sqft_living", "grade", "sqft_above", "sqft_living15", "bathrooms", "bedrooms", "floors", "sqft_lot15", "sqft_lot", "zipcode", "yr_built", "date"]
    
    #saves text entry to entered_text variable when function is called by button press
    entries.append(sqft_living.get())
    entries.append(grade.get())
    entries.append(sqft_above.get())
    entries.append(sqft_living15.get())
    entries.append(bathrooms.get())
    entries.append(bedrooms.get())
    entries.append(floors.get())
    entries.append(sqft_lot15.get())
    entries.append(sqft_lot.get())
    entries.append(zipcode.get())
    entries.append(yr_built.get())
    entries.append(date.get())
    
    entries_df = pd.DataFrame([entries], columns=column_names)
    #clean the data
    entries_df = clean(entries_df)
    
    if all(item!= "" for item in entries): 
        #get prediction
        predicted_price = round(get_prediction(entries_df)[0],2)
        #Clear output text box and output new word to it.
        output.delete(0.0,END)
        output.insert(END, "$"+ format(predicted_price, ","))
        print(predicted_price)
    else:
        output.delete(0.0,END)
        output.insert(END, "Error: Missing Entries")
        print(predicted_price)

#run and make gui work
window = Tk()
window.title("my first")

image = Image.open("../../../images/bill.jpg")
photo = ImageTk.PhotoImage(image)
lbl= Label(window,image=photo)
lbl.pack(pady=0,padx=0)

window.configure(background="blue")
#create header label
Label (window, text="Enter the data:", bg="blue", fg="white", font="none 22 bold") .grid(row=0, column=0, columnspan=2, sticky=W)
#create input labels
input_labels = ['sqft_living', 'grade', 'sqft_above', 'sqft_living15', 'bathrooms', 'bedrooms', 'floors', 'sqft_lot', 'sqft_lot15', 'yr_built', "zipcode", "date"]
i=1
for item in input_labels:
    Label (window, text=item, bg="blue", fg="white", font="none 12 bold") .grid(row=i, column=0, sticky=W)
    i+=1
#create label entry boxes
sqft_living = Entry(window, width=20, bg="white")
sqft_living.grid(row=1, column=1, sticky=W)
sqft_living.insert(0, "1180")
grade = Entry(window, width=20, bg="white")
grade.grid(row=2, column=1, sticky=W)
grade.insert(0, "7")
sqft_above = Entry(window, width=20, bg="white")
sqft_above.grid(row=3, column=1, sticky=W)
sqft_above.insert(0, "1180")
sqft_living15 = Entry(window, width=20, bg="white")
sqft_living15.grid(row=4, column=1, sticky=W)
sqft_living15.insert(0, "1340")
bathrooms = Entry(window, width=20, bg="white")
bathrooms.grid(row=5, column=1, sticky=W)
bathrooms.insert(0, "1")
bedrooms = Entry(window, width=20, bg="white")
bedrooms.grid(row=6, column=1, sticky=W)
bedrooms.insert(0, "3")
floors = Entry(window, width=20, bg="white")
floors.grid(row=7, column=1, sticky=W)
floors.insert(0, "1")
sqft_lot = Entry(window, width=20, bg="white")
sqft_lot.grid(row=8, column=1, sticky=W)
sqft_lot.insert(0, "5650")
sqft_lot15 = Entry(window, width=20, bg="white")
sqft_lot15.grid(row=9, column=1, sticky=W)
sqft_lot15.insert(0, "5650")
yr_built = Entry(window, width=20, bg="white")
yr_built.grid(row=10, column=1, sticky=W)
yr_built.insert(0, "1955")
zipcode = Entry(window, width=20, bg="white")
zipcode.grid(row=11, column=1, sticky=W)
zipcode.insert(0, "98178")
date = Entry(window, width=20, bg="white")
date.grid(row=12, column=1, sticky=W)
date.insert(0, "10/13/2014")
#Add submit button
Button (window, text="SUBMIT", width=6, command=click) .grid(row=len(input_labels)+1,column=0, columnspan=2, sticky=W)
#Add another label
Label (window, text="Predicted Price:", bg="black", fg="white", font="none 20 bold") .grid(row=len(input_labels)+2, column=0,sticky=W)
#text output box
output = Text(window, font="none 20 bold", width=50, height=3, wrap=WORD, background="white")
output.grid(row=len(input_labels)+3, column=0, columnspan=2, sticky=W)
#Run gui loop
window.mainloop()