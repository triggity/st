#!/usr/bin/env python
import fileinput


if __name__ == "__main__":
    print "yes"
    for line in fileinput.input():
        print line
