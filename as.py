import paramiko
import time

router_ip = "172.16.40.1"
username = "test"
password = "Test123456@"

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

                                             
    # Проверяем статус радиомодулей
    shell.send ("wlctl cmds\n")
    time.sleep(2)
    radio_output = shell.recv(65536).decode()
    print("Статус радиомодулей:")
    print(radio_output)

except paramiko.AuthenticationException:
    print("Ошибка аутентификации: неверное имя пользователя или пароль.")
except paramiko.SSHException as e:
    print(f"Ошибка SSH: {e}")
except Exception as e:
    print(f"Не удалось подключиться: {e}")
finally:
    client.close()
