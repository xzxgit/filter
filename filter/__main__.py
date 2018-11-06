#!/usr/bin/python
import csv
import sys
import getopt
import datetime
import time

options = {"file": "", "symbol": "", "company": "", "ex_date_start": "", "ex_date_end": ""}


def printUsage():
    print ('''usage: filter   [-h] [-f <input>] [ -s <symbol>] 
                [ -c <company>]
                [ -b <ex_date_start>]
                [ -e <ex_date_end>]
Optional arguments:
  -h                    help
  -f, --file            The csv file to read
  -s, --symbol          Symbol
  -c, --company         Company name
  -b, --ex_date_start   Filter start date
  -e, --ex_date_end     Filter end date
''')

class Filter(object):
    def __init__(self):
        self.csv_data_list = []
        self.ex_date_start_stamp = 0
        self.ex_date_end_stamp = 0

    def printUsage(self):
        print ('''usage: test.py -i <input> -o <output>
           test.py --in=<input> --out=<output>''')

    def get_csv_data(self):
        csv_file = csv.reader(open(options["file"], 'r'))
        self.csv_data_list = [line for line in csv_file]
        self.csv_data_list.pop(0)

    def filter_by_symbol(self):
        if len(options["symbol"]) != 0:
            self.csv_data_list = [item_data for item_data in self.csv_data_list if
                                  item_data[2] == options["symbol"]]

    def filter_by_company(self):
        if len(options["company"]) != 0:
            self.csv_data_list = [item_data for item_data in self.csv_data_list if
                                  options["company"].lower() in item_data[0].lower()]

    def filter_by_date(self):

        def filter_data(line):
            ex_date_stamp = time.mktime(datetime.datetime.strptime(line[6] , '%Y-%m-%d').timetuple())
            if self.ex_date_start_stamp <= ex_date_stamp and ex_date_stamp <= self.ex_date_end_stamp:
                return line

        ex_date_start = options["ex_date_start"]
        ex_date_end = options["ex_date_end"]
        if ex_date_start != "" and ex_date_end !="":
            self.ex_date_start_stamp = time.mktime(datetime.datetime.strptime(ex_date_start , '%Y-%m-%d').timetuple())
            self.ex_date_end_stamp = time.mktime(datetime.datetime.strptime(ex_date_end, '%Y-%m-%d').timetuple())
            if self.ex_date_start_stamp > self.ex_date_end_stamp:
                print("The params ex_date_start: %s must lower than ex_date_en: %s" % (ex_date_start, ex_date_end))
                exit(-1)
            self.csv_data_list = filter(filter_data, self.csv_data_list)

    def print_result(self):
        self.get_csv_data()
        self.filter_by_symbol()
        self.filter_by_company()
        self.filter_by_date()
        for line in self.csv_data_list:
            print(line)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:s:c:b:e:",
                                   ["file=", "symbol=", "company=", "ex_date_start=",
                                    "ex_date_end "])
    except getopt.GetoptError:
        printUsage()
        sys.exit(-1)
    for opt, arg in opts:
        if opt == '-h':
            printUsage()
            exit(0)
        elif opt in ("-f", "--file"):
            options["file"] = arg
        elif opt in ("-s", "--symbol"):
            options["symbol"] = arg
        elif opt in ("-c", "--company"):
            options["company"] = arg
        elif opt in ("-b", "--ex_date_start"):
            options["ex_date_start"] = arg.replace("\"", "").replace("'", "")
        elif opt in ("-e", "--ex_date_end"):
            options["ex_date_end"] = arg.replace("\"", "").replace("'", "")
    if options["file"] == "":
        print("The -f|--file param is needed")
        printUsage()
        exit(-1)
    filter_data = Filter()
    filter_data.print_result()


if __name__ == "__main__":
    main()