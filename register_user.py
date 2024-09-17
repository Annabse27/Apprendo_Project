import requests

url = 'http://127.0.0.1:8000/api/users/register/'
data = {
    'email': 'test@example.com',
    'password': 'mypassword'
}
response = requests.post(url, json=data)

# Выведем полный ответ от сервера для отладки
print(response.status_code)
print(response.text)  # Покажет полный текст ответа, даже если это HTML

# Попробуем получить JSON только если статус 2xx
try:
    response_json = response.json()
    print(response_json)
except requests.exceptions.JSONDecodeError:
    print("Ошибка: Ответ не в формате JSON")
