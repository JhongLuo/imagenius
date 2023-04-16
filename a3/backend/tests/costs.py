milion = 1000000
thousand = 1000
ten = 10

visits_per_month = 10
month_write = visits_per_month * 5
month_read = visits_per_month * 10

lambda_month_MB_price = (38.78 / 1024) / 24 / 30

price = (0.001) * month_write * 1 * 6
price = lambda_month_MB_price * month_write * 1 * 6
price = (0.25 / milion) * month_write * 1 * 6
print(price)

user = milion
generate = user * 0.3236572
read = user * 7.5e-05
six_month_hours = 24 * 30 * 6
open_search = 4.46 * six_month_hours
total_price = generate + read + open_search
print({"generate": generate, "read": read, "open_search": open_search})
print(total_price)