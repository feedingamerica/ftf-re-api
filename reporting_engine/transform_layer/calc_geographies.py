from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd
import json

# data def 53
def get_direction_traveled(data: 'list[DataFrame]'):
    families = data[1]
    print(str(families.iloc[0]))
    pass

# data def 54
def get_windrose(data: 'list[DataFrame]'):
    pass