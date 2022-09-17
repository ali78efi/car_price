from get_data import get_car_data, str_to_digit
from estimate import predict

user_car = input("enter your car(example: peugeot pars elx-tu5): ")
user_car = user_car.strip(' ').replace(' ', '/')
user_car_year = str_to_digit(input("enter your car model(example: 1399): "))
user_car_usage = str_to_digit(input("enter your car usage(example: 73,000): "))
mode =input('enter x for get available data or enter w for update data: ')
get_car_data(user_car, user_car_year,mode)
predict([user_car, user_car_year, user_car_usage])
