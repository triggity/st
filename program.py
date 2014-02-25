#!/usr/bin/env python
import fileinput
import re

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
    input_group = '==\nTransaction'#:\s(.*)\nOriginator:\s(.*)\nRecipient:\s(.*)\nType:\s(.*)\nAmount:(.*)\n.*'
    matched = re.match(input_group, into, flags=re.DOTALL) 
    print matched.string
    return matched.groupdict()

def main():
    buffer = to_string()
    output = {}
    if not buffer:
        return
    split = split_on_first_transaction(buffer) 
    headers = process_headers(split[0])
    transactions = process_transactions(split[1])
    output.update(headers)

if __name__ == "__main__":
    print "running program"
    print main()
