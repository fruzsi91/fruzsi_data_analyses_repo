import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Load csv files, and create pd dataframes
first_read = pd.read_csv("C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\data_source\\first_read.csv", sep=';', names=['my_date', 'my_time', 'event_type', 'location', 'user_id', 'source', 'topic']) 
return_reads = pd.read_csv("C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\data_source\\return_reads.csv", sep=';', names=['my_date', 'my_time', 'event_type', 'location', 'user_id', 'topic'])

#Modify dataframes for the barchart
first_read_country_2_7 = first_read[(first_read.location == 'country_2') | (first_read.location == 'country_7')].groupby('topic').count()[['user_id']]
return_reads_country_2_7 = return_reads[(return_reads.location == 'country_2') | (return_reads.location == 'country_7')].groupby('topic').count()[['user_id']]
merge_country_2_7 = pd.merge(first_read_country_2_7, return_reads_country_2_7, on = 'topic', how = 'outer')
merge_country_2_7.columns = ['number_of_first_reads', 'number_of_all_return_reads']

# Create the chart

labels = [x for x in merge_country_2_7.index]
first_values = merge_country_2_7['number_of_first_reads'].values
return_values = merge_country_2_7['number_of_all_return_reads'].values
x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars


fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, first_values, width, label='Number of first reads')
rects2 = ax.bar(x + width/2, return_values, width, label='Number of all other (not first) reads')

#ax.set_title('Number of reads and all other (not first) reads by users,\nwho came from country_2 and country_7\n', fontsize=20, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize = 15)
ax.set_ylabel('', fontsize = 8)
ax.legend()
leg = plt.legend(prop={'size': 15})
leg.get_frame().set_edgecolor('black')
leg.get_frame().set_linewidth(1.0)
ax.bar_label(rects1, fontsize = 8, padding=3)
ax.bar_label(rects2, padding=3)
results_path = 'C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\country_2_7_reads.png'
plt.xlabel("Topics", fontsize = 15, fontweight="bold")
plt.show()