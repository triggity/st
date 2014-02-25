import unittest
from mock import patch
import os
import pprint

from st import parsebdi


pp = pprint.PrettyPrinter()
HERE = os.path.abspath(os.path.dirname(__file__))

splits = ['/*BDI*/\nBatch: 99\nDescription: Payroll for January\n', '\nTransaction: 301\nOriginator: 111222333 / 9991\nRecipient: 444555666 / 123456\nType: Credit\nAmount: 10000\n', '\nTransaction: 302\nOriginator: 111222333 / 9991\nRecipient: 123456789 / 55550\nType: Credit\nAmount: 380100\n', '\nTransaction: 305\nOriginator: 111222333 / 9992\nRecipient: 444555666 / 8675309\nType: Debit\nAmount: 999\n', '\n']
def splitgen():
    for i in splits:
        yield i
header_dict = {
    "batch": "99",
    "description": "Payroll for January"
}
transactions= [{'originator': '111222333 / 9991', 'recipient': '444555666 / 123456', 'amount': ' 10000', 'transaction': '301', 'type': 'Credit'}, {'originator': '111222333 / 9991', 'recipient': '123456789 / 55550', 'amount': ' 380100', 'transaction': '302', 'type': 'Credit'}, {'originator': '111222333 / 9992', 'recipient': '444555666 / 8675309', 'amount': ' 999', 'transaction': '305', 'type': 'Debit'}, {}]
class parseBDI(unittest.TestCase):

    def setUp(self):
        outfile = os.path.join(HERE, "fixtures/sample.txt")
        f = open(outfile, "r")
        self.sample = f.read()

    def tearDown(self):
        pass

    def test_split_on_first_transaction(self):
        expected = splits
        result = parsebdi.split_on_first_transaction(self.sample)
        self.assertEqual(result, expected)

    def test_process_headers(self):
        expected =header_dict 
        result = parsebdi.process_headers(splits[0])
        self.assertEqual(result, expected)

    def test_process_headers(self):
        expected = transactions[0]
        result = parsebdi.process_transactions(splits[1])
        self.assertEqual(result, expected)

    @patch("fileinput.input")
    def test_to_dict(self, mockinput):
        mockinput.return_value = splitgen() 
        expected = {}
        expected.update(header_dict)
        expected.update({"transactions": transactions})
        result = parsebdi.to_dict()
        self.assertEqual(result, expected)
