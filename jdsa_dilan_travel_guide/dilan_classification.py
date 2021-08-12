import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt 
#%matplotlib inline
first_read = pd.read_csv("C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\data_source\\first_read.csv", sep=';', names=['my_date', 'my_time', 'event_type', 'location', 'user_id', 'source', 'topic']) 
return_reads = pd.read_csv("C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\data_source\\return_reads.csv", sep=';', names=['my_date', 'my_time', 'event_type', 'location', 'user_id', 'topic'])
subscribes = pd.read_csv("C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\data_source\\subscribes.csv", sep=';', names=['my_date', 'my_time', 'event_type','user_id'])
purchases = pd.read_csv("C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\data_source\\purchases.csv", sep=';', names=['my_date', 'my_time', 'event_type','user_id', 'price'])
                              
reads = return_reads.groupby('user_id').count()[['topic']]
reads.columns = ['number_of_reads']
first_read = first_read[['user_id', 'location','source']]
visitors_data = pd.merge(first_read, reads, on = 'user_id', how = 'inner')
subscribes = subscribes[['user_id', 'event_type']]
visitor_subscribe = pd.merge(visitors_data, subscribes, on = 'user_id', how = 'left')
big_table = visitor_subscribe.fillna(value = 0)
big_table['event_type'] = big_table['event_type'].replace(['subscribe'],'1')
big_table = big_table.astype({"event_type":'int64'}) 

location_dictionary = {'country_1': 1, 'country_2': 2, 'country_3': 3, 'country_4': 4, 'country_5': 5, 'country_6': 6, 'country_7': 7, 'country_8': 8}
source_dictionary = {'Reddit': 0, 'SEO': 1, 'AdWords': 2}
#subscribe_dictionary = {'subscribe': 1}
big_table['location'] = big_table['location'].map(location_dictionary)
big_table['source'] = big_table['source'].map(source_dictionary)
#big_table['event_type'] = big_table['event_type'].map(subscribe_dictionary)


from sklearn.ensemble import RandomForestClassifier
x = big_table[['location', 'source', 'number_of_reads']]
y = big_table['event_type']
model = RandomForestClassifier(n_estimators = 100)
model = model.fit(x, y)

#sample_user = [4, 0, 15]
#print(model.predict([sample_user]))
predict_table = big_table[['user_id', 'location','source','number_of_reads']]

classified_values = []
user_id = []
for index, row in predict_table.iterrows():
    classified_values.append(int(model.predict([[row['location'], row['source'], row['number_of_reads']]])))
    user_id.append(row['user_id'])


list_of_classified_values = list(zip(classified_values, user_id))   
classified_values_table = pd.DataFrame(list_of_classified_values,columns = ['classified_event', 'user_id']) 
result_merge = pd.merge(big_table, classified_values_table, on = 'user_id')
results_merge_list = result_merge[(result_merge.event_type == 0) & (result_merge.classified_event == 1)]
results_merge_list.to_csv("C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\dilan_classification.csv", sep=';', encoding='utf-8', header=True, index=False)

real_values=list(big_table['event_type'])


right = 0
wrong = 0
for i in range(0,66231):
    if classified_values[i] == real_values[i]:
        right = right + 1
    else:
        wrong = wrong + 1

print(right / (wrong + right))