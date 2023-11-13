# Доработать функцию из предыдущего задания таким образом, чтобы
# у неё появился дополнительный режим работы, в котором вывод
# разбивается на слова с удалением всех знаков пунктуации
# (их можно взять из списка string.punctuation модуля string).
# В этом режиме должно проверяться наличие слова в выводе.

import string
import subprocess


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    result_out = result.stdout
    if result.returncode == 0:
        tab = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
        out = result_out.translate(tab).split('\n')
        for i in out:
            print(i)
        if text in out:
            print(f'Comand: {cmd} - completed. Find: {text}')
            return True
        else:
            print(f'Comand: {cmd} - completed. Not find: {text}')
            return False


if __name__ == '__main__':
    checkout('cat /etc/os-release', 'VERSION="22.04.1 LTS (Jammy Jellyfish)"')
