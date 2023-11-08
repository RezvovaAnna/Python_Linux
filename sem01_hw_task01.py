# Условие:
# Написать функцию на Python, которой передаются в качестве параметров команда и текст.
# Функция должна возвращать True, если команда успешно выполнена и текст найден в её
# выводе и False в противном случае. Передаваться должна только одна строка, разбиение
# вывода использовать не нужно.

import subprocess


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    print(result.stdout)
    if text in result.stdout and result.returncode == 0:
        print(f'Comand: {cmd} - completed. Find: {text}')
        return True
    else:
        print(f'Comand: {cmd} - completed. Not find: {text}')
        return False


if __name__ == '__main__':
    checkout('cat /etc/os-release', 'VERSION="22.04.1 LTS (Jammy Jellyfish)"')
