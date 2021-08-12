import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Load csv files, and create pd dataframes
purchases = pd.read_csv("C:\\Users\\Fru\\Desktop\\data_science_20210412\\final_task\\data_source\\purchases.csv", sep=';', names=['my_date', 'my_time', 'event_type','user_id', 'price'])
p_daily_revenue = purchases.groupby('my_date').sum()[['price']].reset_index(drop = True)

#Defining x and y values:
x = p_daily_revenue.index
y = p_daily_revenue.values
x_max = max(x)

# Fitting the Linear Regression model:
coefs = np.polyfit(x, y, 3) 
coefs = np.squeeze(coefs)
predict = np.poly1d(coefs) 

#Getting the R-squared value for the Linear Regression model
from sklearn.metrics import r2_score
r2 = r2_score(y, predict(x))

#STEP 6: Visualing Data at the model
x_test = np.linspace(0, x_max)
y_pred = predict(x_test[:, None])
plt.scatter(x, y)
plt.plot(x_test, y_pred, c = 'r')
plt.text(-3,7400, 'R-squared = %0.2f' % r2)
plt.show()


# Predict the next month's revenue
predict_revenue_next_month = 0
day = x_max + 2

for i in range(1,30):
    predict_daily_revenue =predict(day)
    predict_revenue_next_month += predict_daily_revenue
    day += 1

print(predict_revenue_next_month)

    