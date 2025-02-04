import streamlit as st
import pandas as pd
from datetime import date
from ipyvizzu import Config, Data, Style
from ipyvizzustory import Story, Slide, Step

# Set page configuration for Streamlit app
st.set_page_config(
    page_title="Vizzu - Life Expectancy", #Page title
    page_icon="😊", # Icon
    layout="wide", # Layout type    
)

# Define color palette
color_pallete = {
                    "blue":"#00adf6",
                    "red": "#ee141c",
                    "black":"#000000",
                    "yellow":"#cfd001",
                    "green":"#04a947"
                }

# Get list of countries from secrets and define gender options
countries =st.secrets["countries"]
gender = ["Male","Female"]

# Cache the data generation function to improve performance
@st.cache_data
def generateDataItem(Slide,Step,category,value,color=None,label=None,lightness=None,duration=None,title=None,subtitle=None):
    return {
        "Slide": [Slide],
        "Step": [Step],
        "category": [category],
        "value": [value],
        "color": [color],
        "label": [label],
        "lightness": [lightness],
        "duration": [duration],
        "title": [title],
        "subtitle": [subtitle]
    }

def generateData(df,dfCountry,age,country,year):  
    """Generates the dataframe for the Vizzu story."""  
    dfData = pd.DataFrame() # Initialize an empty dataframe
    
    # Calculate life expectancy, remaining years, and percentages
    lifeExpectancy=round(float(df[df["Country"]==country]["age_0"].values[0]),0)
    remainingYears =  lifeExpectancy-age
    percentageLived = round((age/lifeExpectancy)*100,1)
    percentageRemaining=round(100-percentageLived,1)
    item=generateDataItem(1,1,country,lifeExpectancy,title=f"Life expectancy at birth in {country} in {year}")
    dfData = pd.concat([dfData,pd.DataFrame(item)])
    
    # Generate data items for each slide and step
    item=generateDataItem(2,1,"You",age,title=f"You are now {age} years old")
    dfData = pd.concat([dfData,pd.DataFrame(item)])
    
    item=generateDataItem(3,1,"Years lived",age,title=f"You have {remainingYears:,.0f} years remaining, according to your life expectancy at birth in {country}")
    dfData = pd.concat([dfData,pd.DataFrame(item)])
    item=generateDataItem(3,1,"Years Remaining",remainingYears)
    dfData = pd.concat([dfData,pd.DataFrame(item)])
    
    item=generateDataItem(4,1,"Lived",percentageLived,title=f"Then, you have lived the {percentageLived} % of your life in {country}")
    dfData = pd.concat([dfData,pd.DataFrame(item)])
    item=generateDataItem(4,1,"Remaining",percentageRemaining)
    dfData = pd.concat([dfData,pd.DataFrame(item)])
    position=None
    
    # Generate data items for country ranking
    sortedCountries =df.sort_values("age_0", ascending=False).reset_index(drop=True)    
    for index, row in sortedCountries.iterrows():
        if row["Country"]==country:
            lightness="yes"
            position=index+1            
        else:
            lightness="no"
        title=None
        if index==0:
            title=country
        item=generateDataItem(5,index+1,row["Country"],row["age_0"],lightness=lightness,title=title)
        dfData = pd.concat([dfData,pd.DataFrame(item)])
    # Add dynamic title for the first step
    dfData.loc[(dfData["title"]==country),"title"]=f"{country}'s life expectancy is in the {position} position in the world for {year}"
    
    # Generate data items for life expectancy over past decades
    yearsRange = [year, year - 10, year - 20, year - 30]
    dfYears=dfCountry[dfCountry["Year"].isin(yearsRange)].reset_index(drop=True)

    for index, row in dfYears.sort_values("Year",ascending=False).iterrows():
        if row["Year"]==year:
            lightness="yes"        
        else:
            lightness="no"
        title=None
        if index==0:
            title=country
        item=generateDataItem(6,index+1,str(row["Year"]).replace(".0",""),row["age_0"],lightness=lightness,title=title)
        dfData = pd.concat([dfData,pd.DataFrame(item)])
    dfData.loc[(dfData["title"]==country),"title"]=f"This is how life expectancy in {country} has evolved in the decades prior {year}"

    # Generate data items for life expectancy from birth year to current age + birth year
    dfYears=dfCountry[(dfCountry["Year"]>=year) & (dfCountry["Year"]<=year+age)].sort_values("Year").reset_index(drop=True)
    for index, row in dfYears.iterrows():
        if row["Year"]==year+age:
            lightness="yes"        
        else:
            lightness="no"
        title=None
        if index==0:
            title=country
                
        item=generateDataItem(7,index+1,str(row["Year"]).replace(".0",""),row["age_0"],lightness=lightness,title=title)
        dfData = pd.concat([dfData,pd.DataFrame(item)])
    dfData.loc[(dfData["title"]==country),"title"]=f"This is how life expectancy in {country} has changed since you were born"
    
    return dfData

def getLifeExpectancyData(par_gender,par_year,age,par_country):
    """Reads and preprocesses life expectancy data from CSV files."""
    # Read the appropriate CSV file based on gender
    if par_gender=="Male":
        # dfLifeExpectancyds = pd.read_csv("data-life-expectancy\life-expectancy-male.csv")
        dfLifeExpectancyds = pd.read_csv("https://drive.google.com/uc?id=1a2oBiEpgbPVR0dl2c0MHZivPwY5rBR0L")        
    else:
        # dfLifeExpectancyds = pd.read_csv("data-life-expectancy\life-expectancy-female.csv")    
        dfLifeExpectancyds = pd.read_csv("https://drive.google.com/uc?id=1gisGMkjjE61WiXlLi2g0pyq7nzppImYd")        
    
    # Filter data for the selected year and country type
    dfLifeExpectancy=dfLifeExpectancyds[(dfLifeExpectancyds["Year"]==par_year) & (dfLifeExpectancyds["Type"]=="Country/Area")]    
    dfLifeExpectancy=dfLifeExpectancy[["Region, subregion, country or area *","0",str(age)]]    
    dfLifeExpectancy.columns=["Country","age_0",f"age_{age}"]    
    dfLifeExpectancy["age_0"]=dfLifeExpectancy["age_0"].astype(float)
    
    # Filter data for the selected country across all years
    dfLifeExpectancyCountry=dfLifeExpectancyds[(dfLifeExpectancyds["Region, subregion, country or area *"]==par_country)]    
    dfLifeExpectancyCountry=dfLifeExpectancyCountry[["Year","0",str(age)]]    
    dfLifeExpectancyCountry.columns=["Year","age_0",f"age_{age}"]    
    dfLifeExpectancyCountry["age_0"]=dfLifeExpectancyCountry["age_0"].astype(float)
    return dfLifeExpectancy, dfLifeExpectancyCountry


def calculateAge(birthDate):
    """Calculates age based on birth date."""
    today = date.today()
    age = today.year - birthDate.year -((today.month, today.day) <(birthDate.month, birthDate.day)) 
    return age
# Streamlit app starts here
st.header("Whats your life expectancy?")

# Create input fields for country, birth date, and gender
cols = st.columns(3)
with cols[0]:
    par_country = st.selectbox("Country",options=sorted(countries))
with cols[1]:
    par_birthdate = st.date_input("Birth Date",min_value=date(1950,1,1))
with cols[2]:
    par_gender = st.radio("Gender",options=gender,horizontal=True)

# Generate button    
btnGenerate = st.button("Generate Story",type='primary')

# Generate and display the Vizzu story when the button is clicked
if btnGenerate:        
    age=calculateAge(par_birthdate)
    dfData,dfDataCountry = getLifeExpectancyData(par_gender,par_birthdate.year,age,par_country)

    # Define data types for the dataframe
    d_types = {
        "Slide": str,
        "Step": str,
        "category": str,
        "value": float,
        "color": str,
        "label": str,
        "lightness": str,
        "duration": float,
        "title": str,
        "subtitle": str,
    }
    
    # Generate the data for the visualization
    df = generateData(dfData,dfDataCountry,age,par_country,par_birthdate.year)
    
    # Create Vizzu Data object and add the dataframe
    data = Data()
    data.add_df(df)

    # Create Vizzu Story object and configure it
    story = Story(data)
    story.set_size("100%", "600px")
    story.set_feature("tooltip", True)
    
    # Slide 1 - Life expectancy at birth
    dfSlide = df[df["Slide"]==1]
    title=dfSlide[dfSlide["Step"]==1]['title'].values[0]
    story.add_slide(
        Slide(
            Step(
                Data.filter("(record['Slide'] == '1')"),
                Config(
                    {
                        "coordSystem": "cartesian",
                        "geometry": "rectangle",
                        # "x": "category",
                        "x": {"set": "value", "range": {"min": "0", "max": "100"}},
                        "color": None,
                        "lightness": None,
                        "size": None,
                        "noop": None,
                        "split": False,
                        "align": "none",
                        "orientation": "vertical",
                        "label": "value",
                        "sort": "none",
                        "title": title
                    }
                ),
                Style(
                {
                    "title": {
                        "color": color_pallete["black"],
                        "fontWeight": "bold",
                        "fontSize": "2.5em"
                        
                    },
                    "backgroundColor":"#F5F5F5",                   
                    "plot": {
                        "yAxis": {"label": {"numberScale": "shortScaleSymbolUS","color": "#CCCCCC00"},
                                  "title":{"color": "#CCCCCC00"}},
                        "xAxis": {"label": {"numberScale": "shortScaleSymbolUS","color": "#CCCCCC00"},},                        
                        "marker": {
                            "label": {
                                "numberFormat": "prefixed",
                                "maxFractionDigits": "1",
                                "numberScale": "shortScaleSymbolUS",
                                "fontSize": "30px"
                            },
                            "rectangleSpacing": None,
                            "circleMinRadius": 0.005,
                            "borderOpacity": 1,
                            "colorPalette": color_pallete["yellow"],
                        },
                    }
                }
            ),
            )
        )
    )
    
    # Slide 2 - You are now # years old
    dfSlide = df[df["Slide"]==2]
    title=dfSlide[dfSlide["Step"]==1]['title'].values[0]
    slide02=Slide()
    
    slide02.add_step(
        Step(        
            Data.filter("(record['Slide'] == '2')"),
            # Config(
            #     {
            #         "channels": {
            #                         "x": {"detach": ["value"]},                                    
            #                     },
            #     }
            # ),
            duration=0.5,
            x={"easing": "ease-in", "delay": 0},
            y={"delay": 0},
            show={"delay": 0},
            hide={"delay": 0},
            easing="ease-in-out"
        )
    )

    slide02.add_step(
        Step(                    
            Config(
                {
                    "channels": {
                                    "x": {"attach": ["value"]},
                                },
                }
            ),
            duration=0.5,
            x={"easing": "ease-in", "delay": 0},
            y={"delay": 0},
            show={"delay": 0},
            hide={"delay": 0},
            easing="ease-in-out"
        )
    )
    slide02.add_step(
            Step(
                Data.filter("(record['Slide'] == '2')"),
                Config(
                    {
                        "title": title
                    }
                ),
                Style(
                    {
                        "plot": {
                            "yAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                            "xAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                            "marker": {
                                "label": {
                                    "numberFormat": "prefixed",
                                    "maxFractionDigits": "1",
                                    "numberScale": "shortScaleSymbolUS",
                                },
                                "rectangleSpacing": None,
                                "circleMinRadius": 0.005,
                                "borderOpacity": 1,
                                "colorPalette": color_pallete["green"],
                            },
                        }
                    }
                ),
            )
    )
    
    story.add_slide(slide02)
    # Slide 3: You have ## years remaining
    slide03=Slide()
    dfSlide = df[df["Slide"]==3]
    title=dfSlide[dfSlide["Step"]==1]['title'].values[0]
    slide03.add_step(
        Step(                   
            Config(
                {                                        
                    "orientation": "vertical",                    
                }
            ),
            duration=0.5,
            x={"easing": "ease-in", "delay": 0},
            y={"delay": 0},
            show={"delay": 0},
            hide={"delay": 0},
            easing="ease-in-out"
        )
    )
    slide03.add_step(
        Step(    
            # Data.filter("(record['Slide'] == '3')"),
            Config(
                {
                    "channels": {
                                    "x": {"attach": ["value"]}
                                },
                }
            ),                             
            duration=0.5,
            x={"easing": "ease-in", "delay": 0},
            y={"delay": 0},
            show={"delay": 0},
            hide={"delay": 0},
            easing="ease-in-out"
        )
    )
    slide03.add_step(
        Step(    
            Data.filter("(record['Slide'] == '3')"),
            # Config(
            #     {
            #         "channels": {
            #                         "x": {"attach": ["value"]}
            #                     },
            #     }
            # ),                             
            duration=0.5,
            x={"easing": "ease-in", "delay": 0},
            y={"delay": 0},
            show={"delay": 0},
            hide={"delay": 0},
            easing="ease-in-out"
        )
    )

    slide03.add_step(
            Step(
                Data.filter("(record['Slide'] == '3')"),
                Config(
                    {
                        "coordSystem": "cartesian",
                        "geometry": "rectangle",
                        "x": ["category", "value"],
                        # "y": {"set": "Slide", "range": {"min": "auto", "max": "110%"}},
                        "color": "category",
                        "lightness": None,
                        "size": None,
                        "noop": None,
                        "split": False,
                        "align": "none",
                        "orientation": "vertical",
                        "label": "value",
                        "sort": "none",
                        "legend":None,
                        "title":title
                    }
                ),
                Style(
                    {
                        "plot": {
                            "yAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                            "xAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                            "marker": {
                                "label": {
                                    "numberFormat": "prefixed",
                                    "maxFractionDigits": "1",
                                    "numberScale": "shortScaleSymbolUS",
                                },
                                "rectangleSpacing": None,
                                "circleMinRadius": 0.005,
                                "borderOpacity": 1,
                                "colorPalette": f'{color_pallete["green"]} {color_pallete["yellow"]}',
                            },
                        }
                    }
                ),
            )
        )

    story.add_slide(slide03)
    # Slide 4: Then, you have lived ## % of your life
    slide04=Slide()
    dfSlide = df[df["Slide"]==4]
    title=dfSlide[dfSlide["Step"]==1]['title'].values[0]    
    
    slide04.add_step(
        Step(       
            # Data.filter("(record['Slide'] == '4')"),          
            Config(
                {
                    "coordSystem": "polar",                    
                }
            ),
            duration=0.5,
            x={"easing": "ease-in", "delay": 0},
            y={"delay": 0},
            show={"delay": 0},
            hide={"delay": 0},
            easing="ease-in-out"
        )
    )
    slide04.add_step(
        Step(       
            # Data.filter("(record['Slide'] == '4')"),          
            Config(
                {
                    "channels": {
                                    "x": {"detach": ["category"]},
                                    "color": {"detach": ["category","value"]}
                                },                    
                }
            ),
            duration=0.5,
            x={"easing": "ease-in", "delay": 0},
            y={"delay": 0},
            show={"delay": 0},
            hide={"delay": 0},
            easing="ease-in-out"
        )
    )
    slide04.add_step(
        Step(       
            Data.filter("(record['Slide'] == '4')"),                      
            duration=0.5,
            x={"easing": "ease-in", "delay": 0},
            y={"delay": 0},
            show={"delay": 0},
            hide={"delay": 0},
            easing="ease-in-out"
        )
    )
    slide04.add_step(
            Step(
                Data.filter("(record['Slide'] == '4')"),
                Config(
                    {
                        "coordSystem": "polar",
                        "geometry": "rectangle",
                        "x": ["category", "value"],
                        "y": {"set": None, "range": {"min": "-200%", "max": "100%"}},
                        "color": "category",
                        "lightness": None,
                        "size": None,
                        "noop": None,
                        "split": False,
                        "align": "none",
                        "orientation": "vertical",
                        "label": "value",
                        "sort": "none",
                        "title": title
                    }
                ),
                Style(
                    {
                        "plot": {
                            "yAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                            "xAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                            "marker": {
                                "label": {
                                    "numberFormat": "prefixed",
                                    "maxFractionDigits": "1",
                                    "numberScale": "shortScaleSymbolUS",
                                },
                                "rectangleSpacing": None,
                                "circleMinRadius": 0.005,
                                "borderOpacity": 1,
                                "colorPalette": f'{color_pallete["green"]} {color_pallete["yellow"]}',
                            },
                        }
                    }
                ),
            )
        )
    story.add_slide(slide04)
    
    # Slide 5: Life Expectancy for {country} in {year} was higher
    slide05= Slide()
    dfSlide = df[df["Slide"]==5]
    countryPosition = dfSlide[dfSlide["category"]==par_country]["Step"].values[0]
    lastPosition = dfSlide["Step"].max()
    lowerCountries = dfSlide[dfSlide['Step']>countryPosition]["category"].count()    
    title=f"Life expectancy for {par_country} in {par_birthdate.year} was higher than {lowerCountries} countries"
    slide05.add_step(
        Step(       
            Config(
                {
                 "channels": {
                                    "color": {"detach": ["category"]}, 
                                    # "x":{"detach":["category", "value"]}                                   
                            },
                "x": {"set": None, "range": {"min": "0%", "max": "100%"}},                    
                 }
            ),                      
            duration=0.5,
            x={"easing": "ease-in", "delay": 0},
            y={"delay": 0},
            show={"delay": 0},
            hide={"delay": 0},
            easing="ease-in-out"
        )
    )
    slide05.add_step(
        Step(       
            Config(
                {
                 "coordSystem": "cartesian",
                 "channels": {
                                    # "color": {"detach": ["category"]}, 
                                    "x":{"detach":["category", "value"]}                                   
                            },                    
                 }
            ),                      
            duration=0.5,
            x={"easing": "ease-in", "delay": 0},
            y={"delay": 0},
            show={"delay": 0},
            hide={"delay": 0},
            easing="ease-in-out"
        )
    )
    slide05.add_step(
        Step(
            Data.filter(f"record['Slide'] == '5'"),       
            Config(
                {                    
                    # "channels": {
                    #                 "x": {"attach": ["category","lightness"]},
                    #                 "label": {"detach":"value"}
                    #             }, 
                    "orientation": "horizontal", 
                    "y": {"set": "value", "range": {"min": "auto", "max": "110%"}},            
                }
            ),                      
            duration=0.5,
            x={"easing": "ease-in", "delay": 0},
            y={"delay": 0},
            show={"delay": 0},
            hide={"delay": 0},
            easing="ease-in-out"
        )
    )
    slide05.add_step(
        Step(
            Data.filter(f"record['Slide'] == '5' && record['Step']>={countryPosition}"),       
            Config(
                {                    
                    "channels": {
                                    "x": {"attach": ["category","lightness"]},
                                    "label": {"detach":"value"}
                                }, 
                    "orientation": "horizontal", 
                }
            ),                      
            duration=0.5,
            x={"easing": "ease-in", "delay": 0},
            y={"delay": 0},
            show={"delay": 0},
            hide={"delay": 0},
            easing="ease-in-out"
        )
    )
    slide05.add_step(
        Step(
            # Data.filter(f"record['Slide'] == '5' && record['Step']>={countryPosition}"),       
            Config(
                {                    
                    "channels": {
                                    "x": {"attach": ["category","lightness"]},
                                    "label": {"detach":"value"}
                                }, 
                    "orientation": "horizontal", 
                }
            ),                      
            duration=0.5,
            x={"easing": "ease-in", "delay": 0},
            y={"delay": 0},
            show={"delay": 0},
            hide={"delay": 0},
            easing="ease-in-out"
        )
    )
    slide05.add_step(
            Step(
                Data.filter(f"record['Slide'] == '5' && record['Step']>={countryPosition}"),
                Config(
                    {
                        "coordSystem": "cartesian",
                        "geometry": "rectangle",
                        "x": ["category","lightness"],
                        "y": {"set": "value", "range": {"min": "auto", "max": "110%"}},
                        "color": "lightness",
                        "lightness": None,
                        "size": None,
                        "noop": None,
                        "split": False,
                        "align": "none",
                        # "orientation": "horizontal",
                        "label": None,
                        "sort": "byValue",
                        "reverse": True,
                        "legend":None,
                        "title": title
                    }
                ),
                Style(
                    {
                        "plot": {
                            "yAxis": {"label": {"numberScale": "shortScaleSymbolUS","color":color_pallete["black"]}},
                            "xAxis": {"label": {"numberScale": "shortScaleSymbolUS","angle":1.5708,"color":color_pallete["black"]}},
                            "marker": {
                                "label": {
                                    "numberFormat": "prefixed",
                                    "maxFractionDigits": "1",
                                    "numberScale": "shortScaleSymbolUS",
                                },
                                "rectangleSpacing": None,
                                "circleMinRadius": 0.005,
                                "borderOpacity": 1,
                                "colorPalette": f'{color_pallete["green"]} {color_pallete["blue"]}',
                            },
                        }
                    }
                ),
            )
        )    
    
    story.add_slide(slide05)
    # Slide 6: {Country}'s life expectancy is in the position
    dfSlide = df[df["Slide"]==5]
    title=dfSlide[dfSlide["Step"]==1]['title'].values[0]    
    story.add_slide(
        Slide(
            Step(
                Data.filter(f"record['Slide'] == '5'"),
                Config(
                    {
                        "coordSystem": "cartesian",
                        "geometry": "rectangle",
                        # "x": "category",
                        # "y": {"set": "value", "range": {"min": "auto", "max": "110%"}},
                        "color": "lightness",
                        "lightness": None,
                        "size": None,
                        "noop": None,
                        "split": False,
                        "align": "none",
                        "orientation": "horizontal",
                        "label": None,
                        "sort": "byValue",
                        "reverse": True,
                        "title": title
                    }
                ),
                Style(
                    {
                        "plot": {
                            "yAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                            "xAxis": {"label": {"numberScale": "shortScaleSymbolUS","angle":1.5708}},
                            "marker": {
                                "label": {
                                    "numberFormat": "prefixed",
                                    "maxFractionDigits": "1",
                                    "numberScale": "shortScaleSymbolUS",
                                },
                                "rectangleSpacing": None,
                                "circleMinRadius": 0.005,
                                "borderOpacity": 1,
                                "colorPalette": f'{color_pallete["green"]} {color_pallete["blue"]}',
                            },
                        }
                    }
                ),
            )
        )
    )
    # Slide 7: This is life expectancy in {par_country} compared with he highest and lowest
    title=f"This is life expectancy in {par_country} compared with he highest and lowest in {par_birthdate.year}"
    story.add_slide(
        Slide(
            Step(
                Data.filter(f"record['Slide'] == '5' && (record['Step']=={countryPosition} || record['Step']==1 || record['Step']=={lastPosition})"),
                Config(
                    {
                        "coordSystem": "cartesian",
                        "geometry": "rectangle",
                        # "x": "category",
                        # "y": {"set": "value", "range": {"min": "auto", "max": "110%"}},
                        "color": "lightness",
                        "lightness": None,
                        "size": None,
                        "noop": None,
                        "split": False,
                        "align": "none",
                        "orientation": "horizontal",
                        "label": "value",
                        "sort": "byValue",
                        "reverse": True,
                        "title": title
                    }
                ),
                Style(
                    {
                        "plot": {
                            "yAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                            "xAxis": {"label": {"numberScale": "shortScaleSymbolUS","angle":1.5708}},
                            "marker": {
                                "label": {
                                    "numberFormat": "prefixed",
                                    "maxFractionDigits": "1",
                                    "numberScale": "shortScaleSymbolUS",
                                },
                                "rectangleSpacing": None,
                                "circleMinRadius": 0.005,
                                "borderOpacity": 1,
                                "colorPalette": f'{color_pallete["green"]} {color_pallete["blue"]}',
                            },
                        }
                    }
                ),
            )
        )
    )
    # Slide 8: This is life expectancy in {Country} compared with the highest and lowest
    dfSlide = df[df["Slide"]==6]
    title=dfSlide[dfSlide["Step"]==1]['title'].values[0]
    slide08=Slide()
    slide08.add_step(
        Step(      
            # Data.filter(f"record['Slide'] == '6'"),        
            Config(
                {                    
                    "channels": {
                                    "x": {"detach": ["category","lightness"]},
                                    "color": {"detach":"lightness"}
                                },  
                }
            ),                      
            duration=0.5,
            x={"easing": "ease-in", "delay": 0},
            y={"delay": 0},
            show={"delay": 0},
            hide={"delay": 0},
            easing="ease-in-out"
        )
    )  
    slide08.add_step(
        Step(        
            Data.filter(f"record['Slide'] == '6'"),                          
            duration=0.5,
            x={"easing": "ease-in", "delay": 0},
            y={"delay": 0},
            show={"delay": 0},
            hide={"delay": 0},
            easing="ease-in-out"
        )
    )  
    slide08.add_step(
        Step(      
            # Data.filter(f"record['Slide'] == '6'"),        
            Config(
                {                    
                    "channels": {
                                    "x": {"attach": ["category","lightness"]},
                                    # "color": {"detach":"lightness"}
                                },  
                }
            ),                      
            duration=0.5,
            x={"easing": "ease-in", "delay": 0},
            y={"delay": 0},
            show={"delay": 0},
            hide={"delay": 0},
            easing="ease-in-out"
        )
    )  
 
    slide08.add_step(
            Step(
                Data.filter(f"record['Slide'] == '6'"),
                Config(
                    {
                        "coordSystem": "cartesian",
                        "geometry": "rectangle",
                        # "x": "category",
                        "y": {"set": "value", "range": {"min": "auto", "max": "110%"}},
                        "color": "lightness",
                        "lightness": None,
                        "size": None,
                        "noop": None,
                        "split": False,
                        "align": "none",
                        "orientation": "horizontal",
                        "label": "value",
                        "sort": "none",
                        "reverse": True,
                        "title": title
                    }
                ),
                Style(
                    {
                        "plot": {
                            "yAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                            "xAxis": {"label": {"numberScale": "shortScaleSymbolUS","angle":1.5708}},
                            "marker": {
                                "label": {
                                    "numberFormat": "prefixed",
                                    "maxFractionDigits": "1",
                                    "numberScale": "shortScaleSymbolUS",
                                },
                                "rectangleSpacing": None,
                                "circleMinRadius": 0.005,
                                "borderOpacity": 1,                                
                            },
                        }
                    }
                ),
            )
        )
    story.add_slide(slide08)
    # Slide 9: This is how life expectancy in {country} has evolved
    dfSlide = df[df["Slide"]==7]
    slide09 =Slide()
    title=dfSlide[dfSlide["Step"]==1]['title'].values[0]
    slide09.add_step(
        Step(                  
            Config(
                {                    
                    "channels": {
                                    "x": {"detach": ["category","lightness"]},
                                    "color": {"detach":"lightness"},
                                    "label": {"detach":"value"}
                                },  
                }
            ),                      
            duration=0.5,
            x={"easing": "ease-in", "delay": 0},
            y={"delay": 0},
            show={"delay": 0},
            hide={"delay": 0},
            easing="ease-in-out"
        )
    )  
    slide09.add_step(
        Step(   
            Data.filter(f"record['Slide'] == '7'"),                       
            # Config(
            #     {                    
            #         "channels": {
            #                         "x": {"detach": ["category","lightness"]},
            #                         # "color": {"detach":"lightness"}
            #                     },  
            #     }
            # ),                      
            duration=0.5,
            x={"easing": "ease-in", "delay": 0},
            y={"delay": 0},
            show={"delay": 0},
            hide={"delay": 0},
            easing="ease-in-out"
        )
    )  
    slide09.add_step(
        Step(      
            # Data.filter(f"record['Slide'] == '7'"),        
            Config(
                {                    
                    "channels": {
                                    "x": {"attach": ["category","lightness"]},
                                    "y": {"attach": "value"},
                                    # "color": {"detach":"lightness"}
                                },  
                }
            ),                      
            duration=0.5,
            x={"easing": "ease-in", "delay": 0},
            y={"delay": 0},
            show={"delay": 0},
            hide={"delay": 0},
            easing="ease-in-out"
        )
    )  
    # slide09.add_step(
    #     Step(                      
    #         Config(
    #             {                    
    #                 "channels": {
    #                                 # "x": {"attach": ["category","lightness"]},
    #                                 "color": {"attach":"lightness"}
    #                             },  
    #             }
    #         ),                      
    #         duration=1,
    #         x={"easing": "ease-in", "delay": 0},
    #         y={"delay": 0},
    #         show={"delay": 0},
    #         hide={"delay": 0},
    #         easing="ease-in-out"
    #     )
    # ) 
    slide09.add_step(
            Step(
                Data.filter(f"record['Slide'] == '7'"),
                Config(
                    {
                        "coordSystem": "cartesian",
                        "geometry": "rectangle",
                        "x": ["category","lightness"],
                        "y": {"set": "value", "range": {"min": "auto", "max": "110%"}},
                        "color": "lightness",
                        "lightness": None,
                        "size": None,
                        "noop": None,
                        "split": False,
                        "align": "none",
                        "orientation": "horizontal",
                        "label": None,
                        "sort": "none",
                        "reverse": False,
                        "title": title
                    }
                ),
                Style(
                    {
                        "plot": {
                            "yAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                            "xAxis": {"label": {"numberScale": "shortScaleSymbolUS","angle":1.5708}},
                            "marker": {
                                "label": {
                                    "numberFormat": "prefixed",
                                    "maxFractionDigits": "1",
                                    "numberScale": "shortScaleSymbolUS",
                                },
                                "rectangleSpacing": None,
                                "circleMinRadius": 0.005,
                                "borderOpacity": 1,
                            },
                        }
                    }
                ),
            )
        )

    story.add_slide(slide09)
    
    title="This the life expectancy comparison when you were born until now"
    lastPosition = dfSlide["Step"].max()
    story.add_slide(
        Slide(
            Step(
                Data.filter(f"record['Slide'] == '7' && (record['Step']==1 || record['Step']=={lastPosition})"),
                Config(
                    {
                        "coordSystem": "cartesian",
                        "geometry": "rectangle",
                        "x": ["category","lightness"],
                        "y": {"set": "value", "range": {"min": "auto", "max": "110%"}},
                        "color": "lightness",
                        "lightness": None,
                        "size": None,
                        "noop": None,
                        "split": False,
                        "align": "none",
                        "orientation": "horizontal",
                        "label": "value",
                        "sort": "none",
                        "reverse": False,
                        "title": title
                    }
                ),
                Style(
                    {
                        "plot": {
                            "yAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                            "xAxis": {"label": {"numberScale": "shortScaleSymbolUS","angle":1.5708}},
                            "marker": {
                                "label": {
                                    "numberFormat": "prefixed",
                                    "maxFractionDigits": "1",
                                    "numberScale": "shortScaleSymbolUS",
                                },
                                "rectangleSpacing": None,
                                "circleMinRadius": 0.005,
                                "borderOpacity": 1,
                            },
                        }
                    }
                ),
            )
        )
    )
    story.play()
# pd.read_csv("./life-expectancy-storytelling.csv",sep=";",decimal=',',encoding="latin-1").to_csv('life-expectancy-storytelling-data.csv',index=False)