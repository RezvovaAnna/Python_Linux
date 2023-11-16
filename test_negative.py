import yaml
from checkers import checkout_negative, getout, checkout


with open('config.yaml') as f:
    # читаем документ YAML
    data = yaml.safe_load(f)



class TestNegative:
    def test_step1(self, clear_folders, make_files, make_bad_arx) :
        # test1
        res = []
        res.append(checkout_negative("cd {}; 7z a {}/arxbad.{}".format(data['folder_in'], data['folder_out'], data['type']), "ERROR:"))
        res.append(checkout_negative("cd {}; 7z e  arxbad.{} -o{} -y".format(data['folder_out'], data['folder_test'], data['type']), "ERROR:"))
        assert all(res), "test1 FAIL"


    def test_step2(self, clear_folders, make_files):
        # test2
        res = []
        res.append(checkout("cd {}; 7z a {}/arx2".format(data['folder_in'], data['folder_out']), "Everything is Ok"))
        res.append(checkout_negative("cd {}; 7z e arx3.{}".format(data['folder_out'], data['folder_test']), "ERROR:"))
        assert all(res), "test2 FAIL"




