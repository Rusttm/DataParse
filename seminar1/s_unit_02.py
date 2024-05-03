import requests
import json

# Ваши учетные данные API
client_id = "gbs"
client_secret = "fsq3Zr7uNJN0apGaBntRVkNT2zavThvU+VG4KU42vMuBwko="

# Конечная точка API
endpoint = "https://api.foursquare.com/v3/places/search"

# Определение параметров для запроса API
city = input("Введите название города: ")
params = {
    "client_id": client_id,
    "client_secret": client_secret,
    "near": city,
    "query": "restaurant"
}

headers = {
    "Accept": "application/json",
    "Authorization": "fsq3Zr7uNJN0apGaBntRVkNT2zavThvU+VG4KU42vMuBwko="
}

# Отправка запроса API и получение ответа
response = requests.get(endpoint, params=params,headers=headers)

# Проверка успешности запроса API
if response.status_code == 200:
    print("Успешный запрос API!")
    data = json.loads(response.text)
    venues = data["results"]
    print(venues)
    for venue in venues:
        try:
            print("Название:", venue["name"])
            print("Адрес:", venue["location"]["address"])
            print("\n")
        except Exception as e:
            print(f"Cannot print data, error: {e}")
            print("\n")

else:
    print("Запрос API завершился неудачей с кодом состояния:", response.status_code)
    print(response.text)
