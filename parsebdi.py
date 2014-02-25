#!/usr/bin/env python
import fileinput
import re
import pprint 

pp = pprint.PrettyPrinter()

def split_on_first_transaction(into):
    return into.split("==")

def to_string():
    buffer = ""
    for line in fileinput.input():
        buffer = buffer + line
    return buffer

def process_headers(into):
    input_group = '.*Batch:\s(?P<batch>.*)\nDescription:\s(?P<description>.*)\n'
    matched = re.match(input_group, into, flags=re.DOTALL) 
    return matched.groupdict()

def process_transactions(into):
    input_group = '\nTransaction:\s(?P<transaction>.*)\nOriginator:\s(?P<originator>.*)\nRecipient:\s(?P<recipient>.*)\nType:\s(?P<type>.*)\nAmount:(?P<amount>.*)\n.*'
    matched = re.match(input_group, into, flags=re.DOTALL) 
    if not matched: return {}
    return matched.groupdict() 

def to_dict():
    buffer = to_string()
    output = {}
    if not buffer:
        return
    split = split_on_first_transaction(buffer) 
    headers = process_headers(split[0])
    transactions = [process_transactions(i) for i in split[1:]]
    output.update(headers)
    if transactions: 
         output.update({"transactions": transactions})
    return output

def main():
    dicted = to_dict()
    return dicted

if __name__ == "__main__":
    print main()
