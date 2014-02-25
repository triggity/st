#!/usr/bin/env python
import pprint

import parsebdi

pp = pprint.PrettyPrinter()

def unique_name(routing, acct):
    return routing + acct
def unique_to_parts(name):
    return name[:9], name[9:]
def net_transaction(key, value):
    routing, account = unique_to_parts(key)
    output = {
        "routing_number": routing,
        "account_number": account,
        "net_transactions": value
    }
    return output
def ledger(transactions):
    accounts = {}
    for trx in transactions:
        if trx:
            if (trx["type"] == "Credit"):
              recipient = trx["recipient"] 
              origin = trx["originator"] 
            else:
              recipient = trx["originator"] 
              origin = trx["recipient"] 
            rname = unique_name(*recipient.split(" / "))
            oname = unique_name(*origin.split(" / "))
            if oname not in accounts:
                accounts[oname] = 0
            if rname not in accounts:
                accounts[rname] = 0
            accounts[rname] += int(trx["amount"])
            accounts[oname] -= int(trx["amount"])
    output = [net_transaction(key, value) for (key, value) in accounts.iteritems()]
    return output

def main():
    dicted = parsebdi.to_dict()
    net = ledger(dicted['transactions'])
    output = {
        "batch": dicted["batch"],
        "description": dicted["description"],
        "accounts": net
    }
    pp.pprint(output)
    return output


if __name__ == "__main__":
    main()
