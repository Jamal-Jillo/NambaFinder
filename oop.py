#!/usr/bin/env python3

import argparse
import pymongo
from pymongo import MongoClient


class PhoneNumber:
    """Class to search for phone number operators."""

    def __init__(self, number):
        """Initialize the phone number."""
        self.number = number
        self.digits = None
        self.first_three = None
        self.code = None
        self.collection = None

        self.cluster = MongoClient("mongodb+srv://dbUser:1274@cluster0.1r8epag.mongodb.net/test")
        self.db = self.cluster["NambaFinder"]

    def parse_number(self):
        """Parse the phone number."""
        self.digits = [int(d) for d in str(self.number)]
        self.first_three = int(''.join(str(d) for d in self.digits[:3]))
        if self.first_three == 254:
            self.code = int(''.join(str(d) for d in self.digits[3:6]))
        else:
            self.code = int(''.join(str(d) for d in self.digits[1:4]))

    def validate_number(self):
        """Check phone Number validity."""
        if self.first_three == 254 and len(self.digits) != 12:
            raise ValueError("Invalid number: must be 12 digits for international numbers starting with 254")
        elif self.first_three != 254 and len(self.digits) != 10:
            raise ValueError("Invalid number: must be 10 digits for local numbers")

    def lookup_operator(self):
        """Operator lookup."""
        if self.collection is None:
            self.collection = self.db["Numbers_data"]
        result = self.collection.find_one({"range.start": {"$lte": self.code}, "range.end": {"$gte": self.code}})
        if result:
            return result["operator"]
        else:
            return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='NambaFinder')
    parser.add_argument('Number', help='Enter the number you want to search')
    args = parser.parse_args()
    print("finding number: {} ..".format(args.Number))

    try:
        number = PhoneNumber(args.Number)
        number.parse_number()
        number.validate_number()
        operator = number.lookup_operator()
        if operator:
            print("Phone number belongs to operator:", operator)
        else:
            print("Phone number not found")
    except ValueError as e:
        print(str(e))
