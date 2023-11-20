from checkers import ssh_checkout, ssh_get
import yaml


with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:

    def save_log(self, starttime, name):
        with open(name, 'w') as f:
            f.write(ssh_get(data['host'], data['user'], data['passwd'],"journalctl --since '{}'".format(starttime)))
    def test_step1(self, clear_folders, make_files, start_time):
        # test1
        res = []
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                "cd {}; 7z a {}/arx2 -t{}".format(data['folder_in'], data['folder_out'], data['type']),
                                "Everything is Ok"))
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                "ls {}".format(data['folder_out']), "arx2.{}".format(data['type'])))
        self.save_log(start_time, "log_test_positive_1.txt")
        assert all(res), "test1 FAIL"


    def test_step2(self, clear_folders, make_files, start_time):
        # test2
        res = []
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                "cd {}; 7z a {}/arx2".format(data['folder_in'], data['folder_out']),"Everything is Ok"))
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                "cd {}; 7z e arx2.{} -o{} -y".format(data['folder_out'], data['type'],
                                                                     data['folder_test']), "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(data['host'], data['user'], data['passwd'], "ls {}".format(data["folder_test"]), item))
        self.save_log(start_time, "log_test_positive_2.txt")
        assert all(res), "test2 FAIL"


    def test_step3(self, start_time):
        # test3
        self.save_log(start_time, "log_test_positive_3.txt")
        assert ssh_checkout(data['host'], data['user'], data['passwd'],
                            "cd {}; 7z -t{} t arx2.{}".format(data['folder_out'],
                                                              data['type'], data['type']), "Everything is Ok"), "test3 FAIL"


    def test_step4(self, start_time):
    # test4
        self.save_log(start_time, "log_test_positive_4.txt")
        assert ssh_checkout(data['host'], data['user'], data['passwd'],
                            "cd {}; 7z -t{} u arx2.{}".format(data['folder_in'],
                                                              data['type'], data['type']), "Everything is Ok"), "test4 FAIL"


    def test_step5(self, start_time):
    # test5
        self.save_log(start_time, "log_test_positive_5.txt")
        assert ssh_checkout(data['host'], data['user'], data['passwd'],
                            "cd {}; 7z -t{} d arx2.{}".format(data['folder_out'],
                                                              data['type'], data['type']), "Everything is Ok"), "test5 FAIL"

    def test_step6(self, clear_folders, make_files, start_time):
        # test6 homework seminar_2
        res = []
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                "cd {}; 7z a -t{} {}/arx2.{}" .format(data['folder_in'],
                                                                      data['type'], data['folder_out'], data['type']), "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                    "cd {}; 7z l -t{} arx2.{}".format(data['folder_out'],
                                                                      data['type'], data['type']), item))
        self.save_log(start_time, "log_test_positive_6.txt")
        assert all(res), "test6 FAIL"

    def test_step7(self, clear_folders, make_files, make_subfolder, start_time):
        # test7 homework seminar_2
        res = []
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                "cd {}; 7z a {}/arx2".format(data['folder_in'],
                                                             data['folder_out']), "Everything is Ok"))
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                "cd {}; 7z x arx2.{} -o{} -y".format(data['folder_out'],
                                                                     data['type'], data['folder_test2']), "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(data['host'], data['user'], data['passwd'], "ls {}".format(data["folder_test2"]), item))
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'], "ls {}".format(data["folder_test2"]), make_subfolder[0]))
        self.save_log(start_time, "log_test_positive_7.txt")
        assert all(res), "test7 FAIL"

    def test_step8(self, clear_folders, make_files, start_time):
        #test8
        res = []
        for item in make_files:
            res.append(ssh_checkout(data['host'], data['user'], data['passwd'], "cd {}; 7z h {}".format(data['folder_in'], item),
                                    "Everything is Ok"))
            hash = ssh_get(data['host'], data['user'], data['passwd'],"cd {}; crc32 {}".format(data['folder_in'], item)).upper()
            res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                    "cd {}; 7z h {}".format(data['folder_in'], item), hash))
        self.save_log(start_time, "log_test_positive_8.txt")
        assert all(res), "test8 FAIL"
