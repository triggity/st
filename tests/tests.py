import unittest
from mock import patch
import os
import pprint

from st import parsebdi
from st import program


pp = pprint.PrettyPrinter()
HERE = os.path.abspath(os.path.dirname(__file__))

splits = ['/*BDI*/\nBatch: 99\nDescription: Payroll for January\n', '\nTransaction: 301\nOriginator: 111222333 / 9991\nRecipient: 444555666 / 123456\nType: Credit\nAmount: 10000\n', '\nTransaction: 302\nOriginator: 111222333 / 9991\nRecipient: 123456789 / 55550\nType: Credit\nAmount: 380100\n', '\nTransaction: 305\nOriginator: 111222333 / 9992\nRecipient: 444555666 / 8675309\nType: Debit\nAmount: 999\n', '\n']

header_dict = {
    "batch": "99",
    "description": "Payroll for January"
}
transactions= [{'originator': '111222333 / 9991', 'recipient': '444555666 / 123456', 'amount': ' 10000', 'transaction': '301', 'type': 'Credit'}, {'originator': '111222333 / 9991', 'recipient': '123456789 / 55550', 'amount': ' 380100', 'transaction': '302', 'type': 'Credit'}, {'originator': '111222333 / 9992', 'recipient': '444555666 / 8675309', 'amount': ' 999', 'transaction': '305', 'type': 'Debit'}, {}]

parsed = {'accounts': [{'routing_number': '111222333', 'account_number': '9991', 'net_transactions': -390100}, {'routing_number': '111222333', 'account_number': '9992', 'net_transactions': 999}, {'routing_number': '444555666', 'account_number': '8675309', 'net_transactions': -999}, {'routing_number': '444555666', 'account_number': '123456', 'net_transactions': 10000}, {'routing_number': '123456789', 'account_number': '55550', 'net_transactions': 380100}], 'batch': '99', 'description': 'Payroll for January'}



class parseBDI(unittest.TestCase):

    def setUp(self):
        outfile = os.path.join(HERE, "fixtures/sample.txt")
        f = open(outfile, "r")
        self.sample = f.read()

    def tearDown(self):
        pass

    def mock_input(self):
        for line in self.sample:
            yield line
    def test_split_on_first_transaction(self):
        expected = splits
        result = parsebdi.split_on_transaction(self.sample)
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
        mockinput.return_value = self.mock_input() 
        expected = {}
        expected.update(header_dict)
        expected.update({"transactions": transactions})
        result = parsebdi.to_dict()
        self.assertEqual(result, expected)

    @patch("fileinput.input")
    def test_to_string(self, mockinput):
        mockinput.return_value = self.mock_input() 
        expected = self.sample
        result = parsebdi.to_string()
        self.assertEqual(result, expected)




class ProgramTest(unittest.TestCase):

    def setUp(self):
        self.source = parsed

    def tearDown(self):
        pass

    def test_unqiue_name(self):
        routing = 123456789
        acct = 5555
        expected =  "{}{}".format(routing, acct)
        result = program.unique_name(routing, acct)
        self.assertEqual(result, expected)

    def test_unqiue_to_parts(self):
        routing = '123456789'
        acct = '5555'
        expected = routing, acct
        result = program.unique_to_parts("{}{}".format(routing, acct))
        self.assertEqual(result, expected)

    def test_net_transaction(self):
        key = '1112223339991'
        value = -390100
        expected = parsed["accounts"][0]
        result = program.net_transaction(key, value)
        self.assertEqual(result, expected)
        
    def test_ledger(self):
        expected = parsed["accounts"]
        result = program.ledger(transactions)
        self.assertEqual(result, expected)

    @patch("fileinput.input")
    def test_main(self, mock_input):
        outfile = os.path.join(HERE, "fixtures/sample.txt")
        f = open(outfile, "r")
        sample = f.read()
        def generate():
            for i in sample:
                yield i


        mock_input.return_value = generate()

        expected = parsed
        result = program.main()
        self.assertEqual(result, expected)
