import yaml

from ssh_checkers import ssh_checkout_negative, ssh_checkout, ssh_get

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:

  
    def save_log(self, starttime, name):
        with open(name, 'w') as f:
            f.write(ssh_get(data['host'], data['user'], data['passwd'], "journalctl --since '{}'".format(starttime)))

            
    def test_step1(self, clear_folders, make_files, make_bad_arx, start_time):
        # test1
        res = []
        res.append(ssh_checkout_negative(data['host'], data['user'], data['passwd'],
                                         "cd {}; 7z a {}/arxbad.{}".format(data['folder_in'], data['folder_out'],
                                                                           data['type']), "ERROR:"))
        res.append(ssh_checkout_negative(data['host'], data['user'], data['passwd'],
                                         "cd {}; 7z e  arxbad.{} -o{} -y".format(data['folder_out'],
                                                                                 data['folder_test'], data['type']), "ERROR:"))
        self.save_log(start_time, "log_test_negative_1.txt")
        assert all(res), "test1 FAIL"

        
    def test_step2(self, clear_folders, make_files, start_time):
        # test2
        res = []
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                "cd {}; 7z a {}/arx2".format(data['folder_in'], data['folder_out']),
                                "Everything is Ok"))
        res.append(ssh_checkout_negative(data['host'], data['user'], data['passwd'],
                                         "cd {}; 7z e arx3.{}".format(data['folder_out'], data['folder_test']), "ERROR:"))
        self.save_log(start_time, "log_test_negative_2.txt")
        assert all(res), "test2 FAIL"

