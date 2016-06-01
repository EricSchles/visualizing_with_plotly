from datetime import datetime
import pandas as pd
from collections import OrderedDict

def segment_by_type(values):
    type_one= []
    type_two = []
    for b in values:
        if b.type_one
            type_one.append(b.other_value)
        elif b.type_two:
            type_two.append(b.other_value)
    return [type_one,type_two]

def prepare_for_timeseries(listing):
    year_months = []
    x_vals = []
    y_vals = []
    summation = 0
    for b in listing:
        date = b
        summation += 1#(datetime.now() - date).days
        if not (date.year,date.month) in year_months:
            year_months.append((date.year,date.month))
            x_vals.append(datetime(year=date.year,month=date.month,day=date.day))
            y_vals.append(summation)
            summation = 0
    return x_vals,y_vals

def get_years(dob):
    if not dob:
        return 0
    else:
        time_delta = (datetime.now() - dob)
        return time_delta.days/float(365)

def split_up_ages(ages):
    twenties = len([age for age in ages if age >= 20 and age < 30])
    thirties = len([age for age in ages if age >= 30 and age < 40])
    forties = len([age for age in ages if age >= 40 and age < 50])
    fifties = len([age for age in ages if age >= 50 and age < 60])
    sixties = len([age for age in ages if age >= 60 and age < 70])
    seventies = len([age for age in ages if age >= 70 and age < 80])
    eighties = len([age for age in ages if age >= 80 and age < 90])
    nineties = len([age for age in ages if age >= 90 and age < 100])
    hundreds = len([age for age in ages if age >= 100])
    return twenties,thirties,forties,fifties,sixties,seventies,eighties,nineties,hundreds

def add_month(date):
    if date.month == 12:
        return datetime(year=date.year+1,month=1,day=1)
    else:
        return datetime(year=date.year,month=date.month+1,day=1)


def order_dictionary(dicter):
    return OrderedDict(sorted(dicter.items(), key=lambda t: t[1]))

def differencing():
    timeseries = []
    for b in One.query.all():
        if b.dateA and b.dateB:
            timeseries.append( (b.dateA,(b.dateB - b.dateA).days) )
    timeseries = sorted(timeseries, key=lambda t:t[0])
    return timeseries

def size_of_boxes(timeseries):
    dates = [elem[0] for elem in timeseries]
    month_seperators = [month[0] for month in prepare_for_timeseries(dates,fidelity="month")]
    data = []
    for month_seperator in month_seperators:
        tmp = []
        for elem in timeseries:
            if elem[0].year == month_seperator.year and elem[0].month == month_seperator.month:
                tmp.append(elem[1])
        data.append( [str(month_seperator.year)+"-"+str(month_seperator.month),len(tmp)] )
    return data

def differencing_box_plot(timeseries,name,color):
    dates = [elem[0] for elem in timeseries]
    month_seperators = [month[0] for month in prepare_for_timeseries(dates,fidelity="month")]
    data = []
    for month_seperator in month_seperators:
        tmp = []
        for elem in timeseries:
            if elem[0].year == month_seperator.year and elem[0].month == month_seperator.month:
                tmp.append(elem[1])
        data.append(
            Box(
                y=tmp,
                name=str(month_seperator.year)+"-"+str(month_seperator.month),
                marker=dict(color=color,),
                boxpoints=name
            )
        )
    return data

def prepare_for_box_plot(dates,name,color):
    dates.sort()
    month_seperators = [month[0] for month in prepare_for_timeseries(dates,fidelity="month")]
    timeseries = prepare_for_timeseries(dates,fidelity="day")
    data = []
    for month_seperator in month_seperators:
        tmp = []
        for elem in timeseries:
            if elem[0].year == month_seperator.year and elem[0].month == month_seperator.month:
                tmp.append(elem[1])
        data.append(
            Box(
                y=tmp,
                name=str(month_seperator.year)+"-"+str(month_seperator.month),
                marker=dict(color=color,),
                boxpoints=name
            )
        )
    return data

    
def to_datetime(elem):
    listing = [int(i) for i in elem.split("-")]
    if len(listing) == 2:
        year,month = listing
        day = 1
    elif len(listing) == 3:
        year,month,day = listing
    return datetime(year=year,month=month,day=day)

def series_to_frame(series):
    df = pd.DataFrame()
    for elem in series.iteritems():
        tmp = {}
        tmp["Date"] = elem[0]
        tmp["Count"] = elem[1]
        df = df.append(tmp,ignore_index=True)
    return df

def prepare_for_timeseries(listing,fidelity="month"):
    df = pd.DataFrame()
    for date in listing:
        tmp = {}
        if fidelity == "month":
            tmp["Date"] = str(date.year)+"-"+str(date.month)
        if fidelity == "day":
            tmp["Date"] = str(date.year)+"-"+str(date.month)+"-"+str(date.day)
        df = df.append(tmp,ignore_index=True)
    series = df.groupby(["Date"]).Date.count()
    series = [(to_datetime(elem[0]),elem[1]) for elem in series.iteritems()]
    return sorted(series,key=lambda t:t[0])

def prepare_for_timeseries_weekly(listing):
    listing.sort()
    df = pd.DataFrame()
    tmp = {}
    year,week,day_of_week = datetime.isocalendar(listing[0])
    tmp["year"] = year
    tmp["week"] = week
    tmp["count"] = 1
    tmp["to_order"] = listing[0]
    for date in listing[1:]:
        year,week,day_of_week = datetime.isocalendar(date)
        if tmp["year"] == year and tmp["week"] == week:
            tmp["count"] += 1
        else:
            df = df.append(tmp,ignore_index=True)
            tmp = {}
            tmp["year"] = year
            tmp["week"] = week
            tmp["count"] = 1
            tmp["to_order"] = date
    df = df.drop("week",1)
    df = df.drop("year",1)
    return df
    
def analyze_mappings(mappings):
    final = []
    for ind,mapping in enumerate(mappings):
        tmp = []
        for key in mapping.keys():
            tmp.append(single_val(mapping[key]))
        if not all(tmp):
            print(ind)

def single_val(listing,ind,value):
    for elem in listing[ind+1:]:
        if elem == value:
            return False
    return True

def is_unique(listing):
    """
    if I can uniqueify the values it does so, otherwise returns original list
    """
    for index,value in enumerate(listing):
        if not single_val(listing,index,value):
            return False
    return True

def uniqueify(listing):
    return list(set(listing))

def remove_duplicates(listing):
    new_listing = []
    for elem in listing:
        if not elem in new_listing:
            new_listing.append(elem)
    return new_listing

def clean_mappings(mappings):
    new_mappings = []
    for mapping in mappings:
        tmp = {}
        for key in mapping.keys(): 
            val = uniqueify(mapping[key])
            if len(val) > 1:
                val = remove_duplicates(val)
            tmp[key] = val
        new_mappings.append(tmp)
    return new_mappings

def count_vals(mappings):
    for ind,mapping in enumerate(mappings):
        print(ind)
        print()
        for key in mapping.keys():
            if type(mapping[key]) == type(list()):
                print(key,len(mapping[key]))

def filter_uninteresting_stuff(dicter):
    interesting = []
    #for dicter in dicters:
    if all([val!=1 for val in dicter.values()]):
        interesting.append(dicter)
    return interesting

def impose_order(dicter):
    """
    Expects a dictionary 
    Returns a 2 lists ordered by values in the dictionary, either ascending or descending
    """
    keys = dicter.keys()
    values = dicter.values()
    duplicates = get_duplicates(keys,values)
    mapping = {value:index for index,value in enumerate(values)}
    values.sort()
    new_ordering = []
    duplicate_index = {}.fromkeys(duplicates.keys(),0)
    for value in values:
        if value in duplicates.keys():
            new_ordering.append(duplicates[value][duplicate_index[value]])
            duplicate_index[value] += 1
        else:
            new_ordering.append(mapping[value])
    return values,new_ordering

def get_duplicates(keys,values):
    duplications = {}
    repeat_values = [{index:value} for index,value in enumerate(values) if check_for_duplicates(value,values)]
    for repeat_value in repeat_values:
        key = keys[repeat_value.keys()[0]]
        value = repeat_value.values()[0]
        if not value in duplications.keys():
            duplications[value] = [key]
        else:
            duplications[value].append(key)
    return duplications

        
def check_for_duplicates(value,values):
    listing = values[:]
    for index,elem in enumerate(values):
        if elem == value and elem in listing[index:]:
            return True 
    return False
