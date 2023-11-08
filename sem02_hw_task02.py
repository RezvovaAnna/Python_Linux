# Установить пакет для расчёта crc32
# - sudo apt install libarchive-zip-perl
# Доработать проект, добавив тест команды
# расчёта хеша (h). Проверить, что хеш совпадает с рассчитанным командой crc32.

import subprocess
import zlib


def file_hash(file_path):
    result = 0
    for line in open(file_path, "rb"):
        result = zlib.crc32(line, result)
    return "%x" % (result & 0xFFFFFFFF)


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    print(result.stdout)
    if (text in result.stdout or text in result.stderr) and result.returncode == 0:
        return True
    else:
        return False


def test_crc32():
    name_file = '/home/user/Python_Linux/sem1_task02.py'
    h_file = file_hash(name_file)
    print(h_file)
    assert checkout('crc32 {}'.format(name_file), '{}'.format(h_file)), 'test_crc32 FAIL'
