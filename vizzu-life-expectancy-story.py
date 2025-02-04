import pandas as pd
import pandas as pd
from ipyvizzu import Config, Data, Style
from ipyvizzustory import Story, Slide, Step

df = pd.read_csv('./life-expectancy-story.csv',sep=";",encoding="latin-1",decimal=",")
df.to_csv("life-expectancy-data.csv",index=False)

d_types = {
    "Slide": str,
    "Step": str,
    "category": str,
    "value": float,
    "color": str,
    "label": str,
    "lightness": str,
    "duration": str,
    "title": str,
    "subtitle": str,
}
# df = pd.read_csv('./life-expectancy-story.csv',sep=";",encoding="latin-1")
df = pd.read_csv("life-expectancy-data.csv", dtype=d_types)
# df.to_csv("life-expectancy-data.csv",index=False)
data = Data()
data.add_df(df)
df['title']=df['title'].fillna("")
df['subtitle']=df['subtitle'].fillna("")
story = Story(data)
story.set_size("100%", "600px")
story.set_feature("tooltip", True)

dfSlide = df[df["Slide"]=="1"]
title=dfSlide[dfSlide["Step"]=="1"]['title'].values[0]
story.add_slide(
    Slide(
        Step(
            Data.filter("(record['Slide'] == '1')"),
            Config(
                {
                    "coordSystem": "cartesian",
                    "geometry": "circle",
                    "x": None,
                    "y": {"set": None, "range": {"min": "auto", "max": "auto"}},
                    "color": "category",
                    "lightness": None,
                    "size": "value",
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                    "label": "category",
                    "sort": "none",
                    "legend":None,
                    "title": title
                }
            ),
            Style(
                {
                    "title": {
                        "color": "#025986FF",
                        "fontWeight": "bold",
                        "fontSize": "1.5em"
                        
                    },                   
                    "plot": {
                        "yAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                        "xAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
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
                            "colorPalette": '#16b3e8',                            
                        },
                    }
                }
            ),
        )
    )
)
dfSlide = df[df["Slide"]=="2"]
title=dfSlide[dfSlide["Step"]=="1"]['title'].values[0]
slideHearthbit=Slide()
slidetitle=""
slideSubtitle=""
slideHearthbit.add_step(
    Step(            
            Config(
                    {                           
                        "geometry": "line",
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
for index, row in dfSlide.iterrows():
    step = row["Step"] 
    duration = str(row["duration"]).replace(",",".") 
    title = row["title"]
    if title!="":
        slidetitle=title    
    subtitle= row["subtitle"]
    if subtitle!="":
        slideSubtitle=subtitle
    
    slideHearthbit.add_step(
        Step(
            Data.filter(f"(record['Slide'] == '2') && (record['Step']<={step})"),
            Config(
                {
                    "coordSystem": "cartesian",
                    "geometry": "line",
                    "x": {"set": "Step", "range": {"min": "-0", "max": "33"}},
                    "y": {"set": "value", "range": {"min": "-100", "max": "100"}},
                    "color": None,
                    "lightness": None,
                    "size": None,
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                    "label": None,
                    "sort": "none",
                    "title": slidetitle,
                    "subtitle": slideSubtitle
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
                            "colorPalette": "rgb(102, 197, 204) rgb(246, 207, 113) rgb(248, 156, 116) rgb(220, 176, 242) rgb(135, 197, 95) rgb(158, 185, 243) rgb(254, 136, 177) rgb(201, 219, 116) rgb(139, 224, 164) rgb(180, 151, 231) rgb(179, 179, 179) rgb(136, 204, 238) rgb(204, 102, 119) rgb(221, 204, 119) rgb(17, 119, 51) rgb(51, 34, 136) rgb(170, 68, 153) rgb(68, 170, 153) rgb(153, 153, 51) rgb(136, 34, 85) rgb(102, 17, 0) rgb(136, 136, 136)",
                        },
                    }
                }
            ),
            duration=duration,
            x={"easing": "ease-in-out", "delay": 0},
            y={"delay": 0},
            show={"delay": 0},
            hide={"delay": 0},
            easing="ease-in-out"
        )
    )

story.add_slide(slideHearthbit)

dfSlide = df[df["Slide"]=="3"]
slideLifeExpectancy = Slide()
title=dfSlide[dfSlide["Step"]=="1"]['title'].values[0]
subtitle=dfSlide[dfSlide["Step"]=="1"]['subtitle'].values[0]
slideLifeExpectancy.add_step(
    Step(            
            Config(
                    {                           
                        "geometry": "rectangle",
                        "y": {"set": ["category", "value"],"range": {"min": "auto", "max": "110%"},},
                        "x": {"range": {"min": "auto", "max": "110%"},},
                    }
                ),
            Style(
                {                
                    "plot": {
                        "marker": {
                            "label": {
                                "numberFormat": "prefixed",
                                "maxFractionDigits": "1",
                                "numberScale": "shortScaleSymbolUS",
                                "fontSize": "15px"
                            },
                        },
                    }
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
slideLifeExpectancy.add_step(
    Step(            
            Config(
                    {                           
                        "y": {"set": ["category", "value"],"range": {"min": "auto", "max": "110%"},},
                        "x": {"range": {"min": "auto", "max": "110%"},},
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
slideLifeExpectancy.add_step(
    Step(         
            Data.filter("(record['Slide'] == '3')"),   
            Config(
                    {                           
                        "x": {"detach":"Step"},                        
                        "legend":"color"
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

slideLifeExpectancy.add_step(
        Step(
            Data.filter("(record['Slide'] == '3')"),
            Config(
                {
                    "coordSystem": "cartesian",
                    "geometry": "rectangle",
                    "x": "category",
                    "y": {"set": "value", "range": {"min": "auto", "max": "110%"}},
                    "color": "category",
                    "lightness": None,
                    "size": None,
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                    "label": "value",
                    "sort": "none",
                    "title":title,
                    "subtitle":subtitle
                }
            ),
            Style(
                {
                    "plot": {
                        "yAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                        "xAxis": {"label": {"numberScale": "shortScaleSymbolUS","orientation":"vertical"}},
                        "marker": {
                            "label": {
                                "numberFormat": "prefixed",
                                "maxFractionDigits": "1",
                                "numberScale": "shortScaleSymbolUS",
                            },
                            "rectangleSpacing": None,
                            "circleMinRadius": 0.005,
                            "borderOpacity": 1,
                            # "colorPalette": "#03ae71 #f4941b #f4c204 #d49664 #f25456 #9e67ab #bca604 #846e1c #fc763c #b462ac #f492fc #bc4a94 #9c7ef4 #9c52b4 #6ca2fc #5c6ebc #7c868c #ac968c #4c7450 #ac7a4c #7cae54 #4c7450 #9c1a6c #ac3e94 #b41204",
                        },
                    }
                }
            ),
        )
    )

story.add_slide(slideLifeExpectancy)

dfSlide = df[df["Slide"]=="4"]
slideLifeExpectancy = Slide()
title=dfSlide[dfSlide["Step"]=="1"]['title'].values[0]
subtitle=dfSlide[dfSlide["Step"]=="1"]['subtitle'].values[0]

story.add_slide(
    Slide(
        Step(
            Data.filter("(record['Slide'] == '4')"),
            Config(
                {
                    "coordSystem": "cartesian",
                    "geometry": "rectangle",
                    "x": "category",
                    "y": {"set": "value", "range": {"min": "auto", "max": "110%"}},
                    "color": "category",
                    "lightness": None,
                    "size": None,
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                    "label": "value",
                    "sort": "none",
                    "title":title,
                    "subtitle":subtitle
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
                            # "colorPalette": "#03ae71 #f4941b #f4c204 #d49664 #f25456 #9e67ab #bca604 #846e1c #fc763c #b462ac #f492fc #bc4a94 #9c7ef4 #9c52b4 #6ca2fc #5c6ebc #7c868c #ac968c #4c7450 #ac7a4c #7cae54 #4c7450 #9c1a6c #ac3e94 #b41204",
                        },
                    }
                }
            ),
        )
    )
)

dfSlide = df[(df["Slide"]=="5") & (df["Step"]<="73")]

slideLifeTime=Slide()
slidetitle=""
slideSubtitle=""

for index, row in dfSlide.iterrows():    
    step = row["Step"] 
    year = int(row["label"])    
    age=year-1978
    duration = str(row["duration"]).replace(",",".") 
    title = row["title"]
    
    if int(step)>=73:
        lifePercentage=1
    else:
        lifePercentage = int(step)/73
           
    if title!="":
        slidetitle=f"Year {year}: {age} years old - {title}"
        slideSubtitle=f"Life percentage: {lifePercentage:,.2%}"
    else:
        slidetitle=f"Year {year}: {age} years old - Life percentage: {lifePercentage:,.2%}"
        slideSubtitle=""
        
        
    
    
    
    
    slideLifeTime.add_step(
        Step(
            Data.filter(f"(record['Slide'] == '5') && (record['Step']<={step})"),
            Config(
                {
                    "coordSystem": "cartesian",
                    "geometry": "rectangle",
                    "x": {"set": "Step", "range": {"min": "0", "max": "73"}},
                    "y": {"set": ["category", "value"],"range": {"min": "auto", "max": "110%"},},
                    "color": "category",
                    "lightness": None,
                    "size": None,
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                    "label": None,
                    "sort": "none",
                    "title": slidetitle,
                    "subtitle": slideSubtitle
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
                            "colorPalette": "rgb(102, 197, 204) rgb(246, 207, 113) rgb(248, 156, 116) rgb(220, 176, 242) rgb(135, 197, 95) rgb(158, 185, 243) rgb(254, 136, 177) rgb(201, 219, 116) rgb(139, 224, 164) rgb(180, 151, 231) rgb(179, 179, 179) rgb(136, 204, 238) rgb(204, 102, 119) rgb(221, 204, 119) rgb(17, 119, 51) rgb(51, 34, 136) rgb(170, 68, 153) rgb(68, 170, 153) rgb(153, 153, 51) rgb(136, 34, 85) rgb(102, 17, 0) rgb(136, 136, 136)",
                        },
                    }
                }
            ),
            duration=duration,
            x={"easing": "ease-in-out", "delay": 0},
            y={"delay": 0},
            show={"delay": 0},
            hide={"delay": 0},
            easing="ease-in-out"
        )
    )

story.add_slide(slideLifeTime)

story.add_slide(
    Slide(
        Step(
            Data.filter(f"(record['Slide'] == '5') && (record['Step']<=73)"),
            Config(
                {
                    "coordSystem": "cartesian",
                    "geometry": "rectangle",
                    "x": None,
                    "y": {"set": None, "range": {"min": "auto", "max": "auto"}},
                    "color": "category",
                    "lightness": None,
                    "size": ["category", "count()"],
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                    "label": "count()",
                    "sort": "none",
                    "title": "This is your expected life, look how many years you spend in every stage",
                    "subtitle":"Look where you spend most years and think if you really enjoy it"
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
                            # "colorPalette": "#03ae71 #f4941b #f4c204 #d49664 #f25456 #9e67ab #bca604 #846e1c #fc763c #b462ac #f492fc #bc4a94 #9c7ef4 #9c52b4 #6ca2fc #5c6ebc #7c868c #ac968c #4c7450 #ac7a4c #7cae54 #4c7450 #9c1a6c #ac3e94 #b41204",
                        },
                    }
                }
            ),
        )
    )
)

story.play()