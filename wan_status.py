import paramiko
import time

router_ip = "192.168.1.24"
username = "test"
password = "Test123456@"

try:
    # Создание SSH клиента
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Подключение к маршрутизатору
    client.connect(router_ip, username=username, password=password)
    print("wan status.")

    # Получаем интерактивный сеанс
    shell = client.invoke_shell()
    time.sleep(1)

    # Отправляем команду ifconfig
    shell.send("ifconfig eth4.1\n")
    time.sleep(2)

    # Получаем вывод команды
    output = shell.recv(65536).decode()

    # Разбиваем вывод на строки и ищем первые две строки с полезной информацией
    filtered_lines = []
    for line in output.splitlines():
        if "HWaddr" in line or "inet addr" in line:
            filtered_lines.append(line.strip())
            if len(filtered_lines) == 2:  # Нам нужно только две строки
                break

    # Выводим результат
    if filtered_lines:
        for line in filtered_lines:
            print(line)
    else:
        print("Məlumat tapılmadı HWaddr və ya inet addr.")

except paramiko.AuthenticationException:
    print("Authentication səhvi: Səhv username və ya şifrə.")
except paramiko.SSHException as e:
    print(f"Səhv SSH: {e}")
except Exception as e:
    print(f"Qoşulmaq mümkün olmadı: {e}")
finally:
    client.close()
