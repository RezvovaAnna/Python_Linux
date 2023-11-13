from checkers import checkout, getout
import yaml


with open('config.yaml') as f:
    # читаем документ YAML
    data = yaml.safe_load(f)


class TestPositive:
    def test_step1(self, clear_folders, make_files):
        # test1
        res = []
        res.append(checkout("cd {}; 7z a {}/arx2 -t{}".format(data['folder_in'], data['folder_out'], data['type']),
                            "Everything is Ok"))
        res.append(checkout("ls {}".format(data['folder_out']), "arx2.{}".format(data['type'])))
        assert all(res), "test1 FAIL"


    def test_step2(self, clear_folders, make_files):
        # test2
        res = []
        res.append(checkout("cd {}; 7z a {}/arx2".format(data['folder_in'], data['folder_out']), "Everything is Ok"))
        res.append(checkout("cd {}; 7z e arx2.{} -o{} -y".format(data['folder_out'], data['type'], data['folder_test']), "Everything is Ok"))
        for item in make_files:
            res.append(checkout("ls {}".format(data["folder_test"]), item))
        assert all(res), "test2 FAIL"


    def test_step3(self):
        # test3
        assert checkout("cd {}; 7z -t{} t arx2.{}".format(data['folder_out'],data['type'], data['type']),
                        "Everything is Ok"), "test3 FAIL"


    def test_step4(self):
    # test4
        assert checkout("cd {}; 7z -t{} u arx2.{}".format(data['folder_in'],data['type'], data['type']),
                        "Everything is Ok"), "test4 FAIL"


    def test_step5(self):
    # test5
        assert checkout("cd {}; 7z -t{} d arx2.{}".format(data['folder_out'],data['type'], data['type']),
                        "Everything is Ok"), "test5 FAIL"

    def test_step6(self, clear_folders, make_files):
        # test6 homework seminar_2
        res = []
        res.append(checkout("cd {}; 7z a -t{} {}/arx2.{}" .format(data['folder_in'], data['type'], data['folder_out'], data['type']),
                            "Everything is Ok"))
        for item in make_files:
            res.append(checkout("cd {}; 7z l -t{} arx2.{}".format(data['folder_out'],data['type'], data['type']), item))
        assert all(res), "test6 FAIL"

    def test_step7(self, clear_folders, make_files, make_subfolder):
        # test7 homework seminar_2
        res = []
        res.append(checkout("cd {}; 7z a {}/arx2".format(data['folder_in'], data['folder_out']),
                            "Everything is Ok"))
        res.append(checkout("cd {}; 7z x arx2.{} -o{} -y".format(data['folder_out'], data['type'], data['folder_test2']),
                            "Everything is Ok"))
        for item in make_files:
            res.append(checkout("ls {}".format(data["folder_test2"]), item))
        res.append(checkout("ls {}".format(data["folder_test2"]), make_subfolder[0]))
        assert all(res), "test7 FAIL"

    def test_step8(self, clear_folders, make_files):
        #test8
        res = []
        for item in make_files:
            res.append(checkout("cd {}; 7z h {}".format(data['folder_in'], item), "Everything is Ok"))
            hash = getout("cd {}; crc32 {}".format(data['folder_in'], item)).upper()
            res.append(checkout("cd {}; 7z h {}".format(data['folder_in'], item), hash))
        assert all(res), "test8 FAIL"



