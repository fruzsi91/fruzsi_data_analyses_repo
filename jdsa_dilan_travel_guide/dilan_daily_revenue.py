import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Load csv files, and create pd dataframes
purchases = pd.read_csv("C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\data_source\\purchases.csv", sep=';', names=['my_date', 'my_time', 'event_type','user_id', 'price'])
p_daily_revenue = purchases.groupby('my_date').sum()[['price']].reset_index()
p_daily_revenue.columns = ['date', 'daily_revenue']

#Define the proper sticks for the line chart

date = list(p_daily_revenue.date)
date_X = date[0::7]

# Create the chart

results_path = 'C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\daily_revenue_line_chart.png'
plt.plot(p_daily_revenue['date'], p_daily_revenue['daily_revenue'], color='b', marker='o')
#plt.title("Dilan's tour guide: daily revenue\n", fontsize=18, fontweight="bold")
plt.xticks(date_X, rotation = 90, fontsize=5)
plt.ylabel('Revenue (USD)', fontsize=14, fontweight="bold")
plt.grid(True)
#fig=plt.figure()
plt.savefig(results_path, dpi=600)  
plt.show()   