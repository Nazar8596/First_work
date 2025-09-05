import requests

API_KEY = "e4eeae6311571a0236cb7369a5c8be15"
FULL_URL = "http://api.openweathermap.org/data/2.5/weather"

print("Перевірка погоди ...")

while True:
    city = input("Введіть назву міста: ").strip()
    units = input("Одиниці вимірювання (metric/imperial): ").strip().lower()

    if units not in ["metric", "imperial"]:
        print(" Вказано некоректну одиницю. Використовую 'metric' ...")
        units = 'metric'

    full_url = f"{FULL_URL}?q={city}&appid={API_KEY}&units={units}&lang=ua"

    try:
        r = requests.get(full_url)
        data = r.json()

        if r.status_code == 200:
            print(f"\n Місто:", data["name"], ",", data["sys"]["country"])
            print(" Температура:", data["main"]["temp"], "°C")
            print(" Погода:", data["weather"][0]["description"])
            print(" Вологість:", data["main"]["humidity"], "%")
            print(" Вітер:", data["wind"]["speed"], "м/с\n")
        elif r.status_code == 404:
            print(" Місто не знайдено.")
        else:
            print(f" Сталася помилка. Код: {r.status_code}")
    except Exception as e:
        print(f" Помилка при з'єднанні або обробці даних: ", e)

    again = input("Хочете ще раз? (так/ні): ").strip().lower()
    if again not in ["так", "у", "y", "yes"]:
        print(" Завершено.")
        break