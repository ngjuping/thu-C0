import unittest
from Qinghuiyue.checkers.html_content_checker import check_html_content

class HtmlTestCase(unittest.TestCase):
    right_content=["<h1>非常棒的场地！</h1><p>场地好</p>","<h1>是非常棒的场地</h1><p>vqgbxWdgPakjjrvEZUeBZKKWPQUozRxnnLGwSZOJkeBLFWaInujvULSfqZYRwIgVDdgXhlMEEHPQhmKEdovNUBvaLoBt</p>"]#10字，100字
    wrong_length=["<h1>这是非常棒的场地！</h1>","<h1>是个非常棒的场地!</h1><p>vqgbxWdgPakjjrvEZUeBZKKWPQUozRxnnLGwSZOJkeBLFWaInujvULSfqZYRwIgVDdgXhlMEEHPQhmKEdovNUBvaLoBt</p>"]#9字，101字
    wrong_type=[123]
    wrong_html=["<h1>这是一个非常棒的场地！<h1>","<h1>这是一个非常棒的场地！</h>"]
    def test_right(self):
        for content in self.right_content:
            self.assertEqual(check_html_content(content), (True,"ok"))
        for content in self.wrong_length:
            self.assertEqual(check_html_content(content,9,101),(True,"ok"))
    def test_length(self):

        self.assertEqual(check_html_content(self.wrong_length[0]),(False,"too short"))
        self.assertEqual(check_html_content(self.wrong_length[1]), (False, "too long"))
    def test_type(self):
        for content in self.wrong_type:
            self.assertEqual(check_html_content(content),(False,"wrong type"))
    def test_html(self):
        for content in self.wrong_html:
            self.assertEqual(check_html_content(content),(False,"wrong html"))

if __name__ == '__main__':
    unittest.main()
