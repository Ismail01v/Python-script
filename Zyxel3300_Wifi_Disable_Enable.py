import paramiko
import time
import json  # Импортируем модуль для работы с JSON
import os  # Импортируем модуль для работы с файловой системой

router_ip = "172.16.40.1"
username = "test"
password = "Test123456@"
output_file = r"C:\Users\i.huseynov\Desktop\scrp\wifi_disable.json"  # Путь к файлу JSON


def check_wifi_status(shell):
    # Отправка команды для проверки состояния Wi-Fi
    shell.send("wlctl radio\n")
    time.sleep(1)
    output = shell.recv(65536).decode()
    
    # Получаем предпоследнюю строку для анализа статуса
    return output.splitlines()[-2]

def toggle_wifi(shell, action):
    if action == "disable":
        shell.send("wlctl radio off\n")  # Отключение Wi-Fi
        print("Wi-Fi disable.")
    time.sleep(1)  # Ждем завершения операции

def handle_wifi_button(shell):
    # Проверяем текущий статус Wi-Fi
    wifi_status = check_wifi_status(shell)
    print("Status Wi-Fi now:", wifi_status)

    # Если Wi-Fi включен (может быть 0x0001 или 0x0000)
    if wifi_status in ["0x0001", "0x0000"]:
        print("Wi-Fi включен. Отключаем радио...")
        toggle_wifi(shell, "disable")  # Отключаем Wi-Fi
    else:
        print("Wi-Fi also disable.")

    # Проверяем статус после изменения
    wifi_status_after = check_wifi_status(shell)
    
    # Если после выключения Wi-Fi статус стал 0x0001, предполагаем, что Wi-Fi действительно отключен
    if wifi_status_after == "0x0001":
        print(f"Wi-Fi успешно выключен, но статус изменился на {wifi_status_after} (предполагается, что он отключен).")
    else:
        print("Статус Wi-Fi после изменения:", wifi_status_after)

    # Возвращаем текущий и измененный статус для сохранения
    return wifi_status, wifi_status_after

def load_existing_data(file_path):
    """Загрузить существующие данные из JSON файла."""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    return []  # Вернуть пустой список, если файл не существует

def save_data_to_json(file_path, data):
    """Сохранить данные в JSON файл, добавляя новые записи."""
    existing_data = load_existing_data(file_path)  # Загружаем существующие данные
    existing_data.append(data)  # Добавляем новые данные
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(existing_data, json_file, ensure_ascii=False, indent=4)  # Сохраняем с красивым отступом

try:
    # Создание SSH клиента
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Подключение к маршрутизатору
    client.connect(router_ip, username=username, password=password)
    print("Успешный вход на маршрутизатор.")

    # Получаем интерактивный сеанс
    shell = client.invoke_shell()
    time.sleep(1)  # Даем время на инициализацию

    # Управляем состоянием Wi-Fi через кнопку
    wifi_status_before, wifi_status_after = handle_wifi_button(shell)

    # Подготовка данных для сохранения в JSON
    data = {
        "Статус до изменения": wifi_status_before,
        "Статус после изменения": wifi_status_after + "  off",
        "Router Ip": router_ip
    }
    
    # Отладочный вывод
    print("Данные для сохранения:", data)

    # Сохраняем данные в JSON, добавляя к существующим
    save_data_to_json(output_file, data)

    print(f"Данные успешно экспортированы в {output_file}.")

except paramiko.AuthenticationException:
    print("Ошибка аутентификации: неверное имя пользователя или пароль.")
except paramiko.SSHException as e:
    print(f"Ошибка SSH: {e}")
except Exception as e:
    print(f"Не удалось подключиться: {e}")
finally:
    client.close()
