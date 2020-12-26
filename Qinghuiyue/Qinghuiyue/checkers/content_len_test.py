import unittest
from Qinghuiyue.checkers.content_len_checker import check_content_len

class ContentTestCase(unittest.TestCase):
    right_content=["123","通知标题202012"]#3，10
    wrong_length=["12","通知标题2020123"]#2,11
    wrong_type=[123]
    def test_right(self):
        for content in self.right_content:
            self.assertEqual(check_content_len(content),(True,"ok"))
        for content in self.wrong_length:
            self.assertEqual(check_content_len(content,2,11),(True,"ok"))
    def test_wrong_length(self):
        self.assertEqual(check_content_len(self.wrong_length[0]),(False,"too short"))
        self.assertEqual(check_content_len(self.wrong_length[1]),(False,"too long"))
    def test_wrong_type(self):
        for content in self.wrong_type:
            self.assertEqual(check_content_len(content),(False,"wrong type"))

if __name__ == '__main__':
    unittest.main()
