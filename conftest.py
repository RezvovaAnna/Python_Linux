import random
import string
from datetime import datetime
import pytest
import yaml
from ssh_checkers import ssh_get, ssh_checkout
from file_fun import upload_files

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True)
def make_folders():
    return ssh_checkout(data["host"], data["user"], data["passwd"],
                        "mkdir -p {} {} {} {}".format(data["folder_in"], data["folder_out"], data["folder_test"],
                                                      data["folder_test2"]), "")


@pytest.fixture()
def clear_folders():
    return ssh_checkout(data["host"], data["user"], data["passwd"],
                        "rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_out"], data["folder_test"],
                                                            data["folder_test2"]), "")


@pytest.fixture()
def make_files():
    list_off_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(data["host"], data["user"], data["passwd"],
                        "cd {}; dd if=/dev/urandom of={} bs={} count=1 "
                        "iflag=fullblock".format(data["folder_in"], filename, data['bs']), ""):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout(data["host"], data["user"], data["passwd"],
                        "cd {}; mkdir {}".format(data["folder_in"], subfoldername), ""):
        return None, None
    if not ssh_checkout(data["host"], data["user"], data["passwd"],
                        "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"],
                                                                                                  subfoldername, testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print("Finish: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture()
def make_bad_arx():
    ssh_checkout(data["host"], data["user"], data["passwd"],
                 "cd {}; 7z a {}/arxbad -t{}".format(data["folder_in"], data["folder_out"], data["type"]),"Everything is Ok")
    ssh_checkout(data["host"], data["user"], data["passwd"],
                 "truncate -s 1 {}/arxbad.{}".format(data["folder_out"], data["type"]),"Everything is Ok")
    yield "arxbad.{}".format(data["type"])
    ssh_checkout(data["host"], data["user"], data["passwd"],"rm -f {}/arxbad.{}".format(data["folder_out"], data["type"]), "")


@pytest.fixture(autouse=True)
def deploy_1():
    res = []
    upload_files(data['host'], data['user'], data['passwd'],
                 data['local_path_1'], data['remote_path_1'])
    res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                            "echo {} | sudo -S dpkg -i {}".format(data['passwd'], data['remote_path_1']),
                            'Настраивается пакет'))
    res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                            "echo {} | sudo -S dpkg -s {}".format(data['passwd'], data['package_1']),
                            'Status: install ok installed'))
    if all(res):
        print('Деплой успешен')
        return True
    else:
        print('Ошибка деплоя')
        return False

      
@pytest.fixture(autouse=True)
def deploy_2():
    res = []
    upload_files(data['host'], data['user'], data['passwd'],
                 data['local_path_2'], data['remote_path_2'])
    res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                            "echo {} | sudo -S dpkg -i {}".format(data['passwd'], data['remote_path_2']),
                            'Настраивается пакет'))
    res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                            "echo {} | sudo -S dpkg -s {}".format(data['passwd'], data['package_2']),
                            'Status: install ok installed'))
    print(res)
    if all(res):
        print('Деплой успешен')
        return True
    else:
        print('Ошибка деплоя')
        return False

      
@pytest.fixture()
def start_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  
@pytest.fixture(autouse=True)
def save_stat():
    with open('stat.txt', 'w') as f:
        f.write(ssh_get(data['host'], 'user', '1111', "journalctl --since '{}'".format(datetime.now().strftime("%H:%M:%S.%f"))))

