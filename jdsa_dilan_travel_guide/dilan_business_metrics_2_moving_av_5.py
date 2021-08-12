import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#Load csv files, and create pd dataframes
purchases = pd.read_csv("C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\data_source\\purchases.csv", sep=';', names=['my_date', 'my_time', 'event_type','user_id', 'price'])
#Modify dataframes for the barchart
purchases_8 = purchases[purchases.price == 8].groupby('my_date').count()[['event_type']]
purchases_80 = purchases[purchases.price == 80].groupby('my_date').count()[['event_type']]
purchases_8_date = purchases_8.reset_index()
purchases_8_cal = purchases_8.reset_index(drop = True)

# E-book: calculate moving avarage

count = int(purchases_8_cal['event_type'].count() - 4) # moving_range : must modify!!
index = 2 # moving_range : must modify!!
purchases_8_cal['moving_avarage'] = pd.Series(dtype='float')

for i in range(0,count):

    datas = purchases_8_cal.iloc[[index - 2,index - 1,index,index + 1,index + 2]]['event_type'].tolist() # moving_range : must modify!!
    avarage = f"{sum(datas) / 5:.2f}" # moving_range : must modify!!
    
    purchases_8_cal.at[index, 'moving_avarage'] = avarage
    index += 1

purchases_8_cal_date = pd.merge(purchases_8_cal, purchases_8_date, left_index=True, right_index=True)
purchases_8_cal_date = purchases_8_cal_date[['my_date', 'moving_avarage']]
purchases_8_cal_date = purchases_8_cal_date.dropna()

#Video: calculate moving avarage

purchases_80_date = purchases_80.reset_index()
purchases_80_cal = purchases_80.reset_index(drop = True)
count = int(purchases_80_cal['event_type'].count() - 4)
index = 2
purchases_80_cal['moving_avarage'] = pd.Series(dtype='float')

for i in range(0,count):

    datas = purchases_80_cal.iloc[[index - 2,index - 1,index,index + 1,index + 2]]['event_type'].tolist()
    avarage = f"{sum(datas) / 5:.2f}"

    purchases_80_cal.at[index, 'moving_avarage'] = avarage
    index += 1

purchases_80_cal_date = pd.merge(purchases_80_cal, purchases_80_date, left_index=True, right_index=True)
purchases_80_cal_date = purchases_80_cal_date[['my_date', 'moving_avarage']]
purchases_80_cal_date = purchases_80_cal_date.dropna()

# Create linecharts

fig, ax = plt.subplots()
ax.plot(purchases_8_cal_date['my_date'], purchases_8_cal_date['moving_avarage'], label='e-book')
ax.plot(purchases_80_cal_date['my_date'], purchases_80_cal_date['moving_avarage'], label='video course')
#ax.set_title("Dilan's tour guide: daily amount of sold products\n (with 5-daily moving avarage)", fontsize=18, fontweight="bold")

# define the proper ticks for the line chart
date = list(purchases_8_cal_date['my_date'])
date_X = np.arange(len(date)) # axis x sticks

# define the proper ticklabels for the line chart

list_date = []
index = 0
for i in range(1,86,7): # moving_range : must modify!!
    list_date.append(date[index]) 
    index+=7
    for i in range(1,7):
        list_date.append("")
del list_date[-6:] # moving_range : must modify!!

ax.set_xticks(date_X)
ax.set_xticklabels(list_date, fontsize=8, rotation= 90)
ax.set_ylabel('Number of sold products', fontsize=14, fontweight="bold")
leg = ax.legend(prop={'size': 12}, framealpha=1.0)
leg.get_frame().set_edgecolor('black')
leg.get_frame().set_linewidth(1.0)
plt.grid()
plt.show()