import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#Load csv files, and create pd dataframes
first_read = pd.read_csv("C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\data_source\\first_read.csv", sep=';', names=['my_date', 'my_time', 'event_type', 'location', 'user_id', 'source', 'topic']) 
return_reads = pd.read_csv("C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\data_source\\return_reads.csv", sep=';', names=['my_date', 'my_time', 'event_type', 'location', 'user_id', 'topic'])
subscribes = pd.read_csv("C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\data_source\\subscribes.csv", sep=';', names=['my_date', 'my_time', 'event_type','user_id'])
purchases = pd.read_csv("C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\data_source\\purchases.csv", sep=';', names=['my_date', 'my_time', 'event_type','user_id', 'price'])

#Modify dataframes for the heatmapping
first_read_group = first_read.groupby('location').count()[['user_id']]
return_reads_unique = return_reads.drop_duplicates(subset='user_id')
return_reads_group = return_reads_unique.groupby('location').count()[['user_id']]
subscribes_merge = pd.merge(subscribes, first_read, on = 'user_id')
subscribes_group = subscribes_merge.groupby('location').count()[['user_id']]
purchases_merge = pd.merge(purchases, first_read, on = 'user_id')
purchases_merge_unique = purchases_merge.drop_duplicates(subset='user_id')
purchases_merge_group = purchases_merge_unique.groupby('location').count()[['user_id']]
dilan_merge = first_read_group.merge(return_reads_group, on = 'location').merge(subscribes_group, on = 'location').merge(purchases_merge_group, on = 'location')

#Calculate percantege with chain index method

dilan_merge.columns = ['all_visitors', 'return_visitors', 'subscribers', 'purchasers']
dilan_merge['perc_1'] = dilan_merge['all_visitors'] / dilan_merge['all_visitors'] * 100
dilan_merge['perc_2'] = dilan_merge['return_visitors'] / dilan_merge['all_visitors'] * 100
dilan_merge['perc_3'] = dilan_merge['subscribers'] / dilan_merge['return_visitors'] * 100
dilan_merge['perc_4'] = dilan_merge['purchasers'] / dilan_merge['subscribers'] * 100

# Create the 2 main dataframes

dilan_merge_percent = dilan_merge[['perc_1', 'perc_2', 'perc_3', 'perc_4']]
dilan_merge = dilan_merge[['all_visitors', 'return_visitors', 'subscribers', 'purchasers']]
dilan_merge_percent.columns = ['all_visitors', 'return_visitors', 'subscribers', 'purchasers']
dilan_merge_percent = dilan_merge_percent.astype({"all_visitors":'int', "return_visitors":'int', "subscribers":'int', "purchasers":'int'}) 

# Create the 2 heatmaps
#1
plt.figure(figsize=(15,15))
sns.set(font_scale=1.5)
heatmap = sns.heatmap(dilan_merge, annot=True, annot_kws={"size": 25}, fmt="d",  cmap="Reds")
heatmap.set_yticklabels(heatmap.get_yticklabels(), rotation=360) 
results_path = 'C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\funnel_country_heatmap_.png'
#plt.title('Dilan travel guide: Funnel analysis (location)\n', fontsize = 35, fontweight="bold")
plt.xlabel('Activity of the visitors', fontsize = 25, fontweight="bold")
plt.ylabel('Location of the visitors', fontsize = 25, fontweight="bold")
plt.savefig(results_path, dpi=150)

#2
plt.figure(figsize=(15,15))
sns.set(font_scale=1.5)
heatmap = sns.heatmap(dilan_merge_percent, annot=True, annot_kws={"size": 25}, fmt="d", cmap="Reds")
heatmap.set_yticklabels(heatmap.get_yticklabels(), rotation=360) 
results_path = 'C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\funnel_country_heatmap_percent_.png'
#plt.title('Dilan travel guide: Funnel analysis (location)\n(%, percentage)', fontsize = 35, fontweight="bold")
plt.xlabel('Activity of the visitors', fontsize = 25, fontweight="bold")
plt.ylabel('Location of the visitors', fontsize = 25, fontweight="bold")
plt.savefig(results_path, dpi=150)                                  


