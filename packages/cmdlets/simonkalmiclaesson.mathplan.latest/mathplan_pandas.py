import os
try:
	import pandas as pd
except:
     os.system("python3 -m pip install pandas")
     import pandas as pd

file = f"{CSScriptRoot}{os.sep}Matematik M2_2023.xlsx"

#Read excel file
try:
    df = pd.read_excel(file)
except:
    os.system("python3 -m pip install openpyxl")
    df = pd.read_excel(file)

#Convert dataframe to dictionary
data = df.to_dict(orient='records')

#Reformat the data
output = {"weeks": [{"week_num":week["Week"],
                    week["Day"].lower():[{"Content":week["Content"]},
                                       {"pages":week["pages in book"]},
                                       {"task":week["task"]},
                                       {"task_lower":week["task lower level"]},
                                       {"task_higher":week["task higher level"]},
                                       {"links":week["help links"].split(" ")},
                                       {"info":week["other info"]}]
                   } for week in data ]}


print(output)