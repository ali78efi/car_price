import csv
from sklearn import tree

def predict(user_car_details):
    x = []
    y = []
    with open(f'./cars_data/{user_car_details[0].replace("/","_")}.csv') as cf:
        next(cf)
        data = csv.reader(cf)
        for line in data:
            x.append(line[0:2])
            y.append(line[2])

    
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x, y)

    new_data = [user_car_details[1:]]
    price_predict = clf.predict(new_data)

    print('your car price is:', price_predict[0])
