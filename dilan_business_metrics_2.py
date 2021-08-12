import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Load csv files, and create pd dataframes
purchases = pd.read_csv("C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\data_source\\purchases.csv", sep=';', names=['my_date', 'my_time', 'event_type','user_id', 'price'])
#Modify dataframes for the barchart
purchases_8 = purchases[purchases.price == 8].groupby('my_date').count()[['event_type']]
purchases_80 = purchases[purchases.price == 80].groupby('my_date').count()[['event_type']]

# Create the line charts

fig, ax = plt.subplots()
ax.plot(purchases_8.index, purchases_8['event_type'], label='e-book')
ax.plot(purchases_8.index, purchases_80['event_type'], label='video course')
#ax.set_title("Dilan's tour guide: daily amount of sold products\n", fontsize=18, fontweight="bold")

# define the proper ticks for the line chart
date = list(purchases_8.index)
date_X = np.arange(len(date))
# define the proper ticklabels for the line chart
list_date = []
index = 0
for i in range(1,88,7):
    list_date.append(date[index])
    index+=7
    for i in range(1,7):
        list_date.append("")
del list_date[-2:]

ax.set_xticks(date_X)
ax.set_xticklabels(list_date, fontsize=8, rotation= 90)
ax.set_ylabel('Number of sold products', fontsize=14, fontweight="bold")
leg = ax.legend(prop={'size': 12}, framealpha=1.0)
leg.get_frame().set_edgecolor('black')
leg.get_frame().set_linewidth(1.0)
plt.grid()
plt.show()
