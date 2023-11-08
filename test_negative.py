import subprocess


folder_test = '/home/user/test'
folder_out = '/home/user/out'
folder_in = '/home/user/folder1'


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    print(result.stdout)
    if (text in result.stdout or text in result.stderr) and result.returncode != 0:
        return True
    else:
        return False


def test_step1():
    # test1
    res1 = checkout("cd {}; 7z e arx3.7z -o{} -y".format(folder_out, folder_in), "ERRORS:")
    assert res1, "test1 FAIL"


def test_step2():
    # test2
    assert checkout("cd {}; 7z t arx3.7z".format(folder_out), "ERRORS:"), "test2 FAIL"



