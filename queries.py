#!/usr/bin/env python3


import argparse
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://dbUser:1274@cluster0.1r8epag.mongodb.net/test")
db = cluster["NambaFinder"]
collection = db["Numbers_data"]

# results = collection.find({"operator": "Airtel Networks Kenya Ltd"})

# for result in results:
   # print(result)

parser = argparse.ArgumentParser(description='NambaFinder')
parser.add_argument('Number', help='Enter the number you want to search')

args = parser.parse_args()

print(f"finding number: {args.Number} ")

digits = [int(d) for d in str(args.Number)]  # List

first_three = ''.join(str(d) for d in digits[:3])  # String

first_three = int(first_three)


if first_three == 254:
    if len(digits) == 12:
        code = digits[3:6]
        code = ''.join(str(d) for d in code)
        code = int(code)
        result1 = collection.find_one({"range.start": {"$lte": code}, "range.end": {"$gte": code}})

        if result1:
            print("Phone number belongs to operator:", result1["operator"])
        else:
            print("Phone number not found")
    else:
        print("Incorrect number")
else:
    if len(digits) == 10:
        code = digits[1:4]

        code = ''.join(str(d) for d in code)
        code = int(code)
        result1 = collection.find_one({"range.start": {"$lte": code}, "range.end": {"$gte": code}})

        if result1:
            print("Phone number belongs to operator:", result1["operator"])
        else:
            print("Phone number not found")
    else:
        print("Incorrect number")
