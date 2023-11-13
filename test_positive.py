
import subprocess


folder_test = '/home/user/test'
folder_test2 = '/home/user/test2'
folder_out = '/home/user/out'
folder_in = '/home/user/folder1'


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    print(result.stdout)
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def test_step1():
    # test1
    res1 = checkout("cd {}; 7z a {}/arx2".format(folder_test, folder_out,), "Everything is Ok")
    res2 = checkout("ls {}".format(folder_out), "arx2.7z")
    assert res1 and res2, "test1 FAIL"


def test_step2():
    # test2
    res1 = checkout("cd {}; 7z e arx2.7z -o{} -y".format(folder_test, folder_in), "Everything is Ok")
    res2 = checkout("ls {}".format(folder_in), "test1")
    res3 = checkout("ls {}".format(folder_in), "test2")
    assert res1 and res2 and res3, "test2 FAIL"


def test_step3():
    # test3
    assert checkout("cd {}; 7z t arx2.7z".format(folder_test), "Everything is Ok"), "test3 FAIL"


def test_step4():
    # test4
    assert checkout("cd {}; 7z u arx2.7z".format(folder_test), "Everything is Ok"), "test4 FAIL"


def test_step5():
    # test5
    assert checkout("cd {}; 7z d arx2.7z".format(folder_test), "Everything is Ok"), "test5 FAIL"

def test_step6():
    # test6 homework seminar_2
    res1 = checkout("cd {}; 7z l arx2.7z".format(folder_out, folder_in), "test1.txt")
    res2 = checkout("cd {}; 7z l arx2.7z".format(folder_out, folder_in), "test2.txt")
    assert res1 and res2, "test6 FAIL"

def test_step7():
    # test7 homework seminar_2
    res1 = checkout("cd {}; 7z x arx2.7z -o{} -y".format(folder_out, folder_test2), "Everything is Ok")
    res2 = checkout("ls {}".format(folder_test2), "test1.txt")
    res3 = checkout("ls {}".format(folder_test2), "test2.txt")
    assert res1 and res2 and res3, "test7 FAIL"


