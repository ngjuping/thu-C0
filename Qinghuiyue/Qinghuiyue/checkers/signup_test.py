import unittest
from Qinghuiyue.checkers.signup_checker import check_signup


class SignupTestCase(unittest.TestCase):
    right_api_id = ['2018000000']
    right_name = ['PB', 'qiuyuhanqi']  # 2,10
    wrong_name = [123, 'Q', 'qiuyuhanqiu']
    wrong_api_id = [2018000000, '201800000', '20180000001', '201801239p']
    right_pwd = ['123abc', '1234567890qwertyuiop']
    wrong_pwd = [123456, '123456', 'abcdef', '123ab', '1234567890qwertyuiopa']

    def test_right(self):
        for api_id in self.right_api_id:
            for name in self.right_name:
                for pwd in self.right_pwd:
                    self.assertEqual(check_signup({"api_id": api_id,
                                                   "name": name, "pwd": pwd}), (True, "ok"))

    def test_wrong_api(self):
        for api_id in self.wrong_api_id:
            self.assertEqual(check_signup({"api_id": api_id,
                                           "name": self.right_name[0],
                                           "pwd": self.right_pwd[0]}), (False, "api_id"))
    def test_wrong_name(self):
        for name in self.wrong_name:

            self.assertEqual(check_signup({"api_id": self.right_api_id[0],
                                           "name": name,
                                           "pwd": self.right_pwd[0]}), (False, "name"))
    def test_wrong_pwd(self):
        for pwd in self.wrong_pwd:
            self.assertEqual(check_signup({"api_id": self.right_api_id[0],
                                           "name": self.right_name[0],
                                           "pwd": pwd}), (False, "pwd"))

if __name__ == '__main__':
    unittest.main()
