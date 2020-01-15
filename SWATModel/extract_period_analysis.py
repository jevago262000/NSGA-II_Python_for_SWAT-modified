import pandas as pd
import os, sys
from dateutil.relativedelta import relativedelta
import datetime

script_location = os.path.dirname(sys.argv[0])

def Reduce(values, epd):
    new_values = []

    indate = datetime.date(epd.iy, epd.im, 1)
    findate = datetime.date(epd.fy, epd.fm, 1)
    mths_period = pd.date_range(indate, findate, freq='MS').strftime("%m").tolist()
    mths_period = [int(x) for x in mths_period]

    d = {'months':mths_period, 'values':values}
    df = pd.DataFrame(d)

    new_values = df[df.months.isin(epd.mths)]['values'].tolist()
    return new_values


class Get_Values:
    def __init__(self, file_name):
        file_extract = open(os.path.join(script_location, file_name), 'r')
        lines = file_extract.readlines()

        mths = lines[1].split("=")[1].replace(" ", "").replace("\n", "").split(",")
        mths = [int(x) for x in mths]
        im = int(lines[2].split("=")[1].replace(" ", ""))
        fm = int(lines[3].split("=")[1].replace(" ", ""))
        iy = int(lines[4].split("=")[1].replace(" ", ""))
        fy = int(lines[5].split("=")[1].replace(" ", ""))

        file_extract.close()

        self.mths = mths
        self.im = im
        self.fm = fm
        self.iy = iy
        self.fy = fy