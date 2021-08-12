import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Load csv files, and create pd dataframes
first_read = pd.read_csv("C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\data_source\\first_read.csv", sep=';', names=['my_date', 'my_time', 'event_type', 'location', 'user_id', 'source', 'topic']) 
return_reads = pd.read_csv("C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\data_source\\return_reads.csv", sep=';', names=['my_date', 'my_time', 'event_type', 'location', 'user_id', 'topic'])

#Modify dataframes for the pie chart
first_read_country_2_7 = first_read[(first_read.location == 'country_2') | (first_read.location == 'country_7')].groupby('source').count()[['user_id']]
return_reads_country_2_7 = return_reads[(return_reads.location == 'country_2') | (return_reads.location == 'country_7')][['user_id']]
return_reads_country_2_7_unique = return_reads_country_2_7.drop_duplicates(subset='user_id')
return_reads_country_2_7_unique.reset_index()
return_reads_merge = pd.merge(return_reads_country_2_7_unique, first_read, on = 'user_id', how = 'left')
return_reads_merge_group = return_reads_merge.groupby('source').count()[['user_id']]

#Create the values and the labels of the values for the pie chart

first_read_values = first_read_country_2_7['user_id'].values
first_read_label_data = [int(x) for x in first_read_values]
first_read_label = [x for x in first_read_country_2_7.index]

return_reads_values = return_reads_merge_group['user_id'].values
return_reads_label_data = [int(x) for x in return_reads_values]
return_reads_label = [x for x in return_reads_merge_group.index]

#This function calculates percentage values that will show on the pie chart
def func(pct, allvals):
    absolute = float(pct/100.*np.sum(allvals))
    
    return "{:.1f}%\n{:.0f} users".format(pct, absolute)

# Create the charts

mylabels = ["AdWords", "Reddit", "SEO"]
results_path = 'C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\country_2_7_pie_chart_all.png'
fig1, ax1 = plt.subplots()
ax1.pie(first_read_values, labels = mylabels, autopct=lambda pct: func(pct, first_read_label_data),textprops=dict(color="w"))
ax1.legend(return_reads_label, title = 'Sources', loc="center left",bbox_to_anchor=(1, 0, 0.5, 1))
#x1.set_title("Pie Chart - Sources of the first visitors")
plt.savefig(results_path, dpi=150)   

mylabels = ["AdWords", "Reddit", "SEO"]
results_path = 'C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\country_2_7_pie_chart_return.png'
fig1, ax1 = plt.subplots()
ax1.pie(return_reads_values, labels = mylabels, autopct=lambda pct: func(pct, return_reads_label_data),textprops=dict(color="w"))
ax1.legend(return_reads_label, title = 'Sources', loc="center left",bbox_to_anchor=(1, 0, 0.5, 1))
#ax1.set_title("Pie Chart - Sources of the return visitors")
plt.savefig(results_path, dpi=150)  