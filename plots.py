import shutil
from collections import OrderedDict
from helpers import *
import pandas as pd
import plotly
from plotly.graph_objs import Bar,Layout,Scatter, Box, Annotation,Marker,Font,XAxis,YAxis
import scipy as sp
from scipy.stats import describe
from datetime import datetime
import numpy as np
from statsmodels.api import formula 
from app.models import Issues
import plotly
from plotly.graph_objs import Bar,Layout
import scipy as sp
from scipy.stats import describe
import code
import shutil
from num2words import num2words

def age_freq_plot(ages,filename):
    n = len(ages)
    plotly.offline.plot({
        "data":[Bar(x=["20-30","30-40","40-50","50-60","60-70","70-80","80-90","90-100"],y=ages,text="ages")],
        "layout":Layout(
            title="Frequencies of age segmentation; number of observations="+str(n)
            )
        })
    shutil.move("temp-plot.html",filename)

def box_plot(dates,date_type,filename):
    n = len(dates)
    dates.sort()
    month_seperators = [month[0] for month in prepare_for_timeseries(dates,fidelity="month")]
    timeseries = prepare_for_timeseries(dates,fidelity="day")
    data = []
    for month_seperator in month_seperators:
        tmp = []
        for elem in timeseries:
            if elem[0].year == month_seperator.year and elem[0].month == month_seperator.month:
                tmp.append(elem[1])
        data.append(Box(y=tmp,name=str(month_seperator.year)+"-"+str(month_seperator.month)))        
    plotly.offline.plot({
        "data":data
        ,"layout":Layout(
          title=date_type+" per month over time showing the distribution over the month; number of observations="+str(n)
            )
        })
    shutil.move("temp-plot.html",filename)


def bar_chart_plot(box_sizes,filename):
    n = sum([elem[1] for elem in box_sizes])
    plotly.offline.plot({
        "data":[Bar(x=[elem[0] for elem in box_sizes],y=[elem[1] for elem in box_sizes])]
        ,"layout":Layout(
            title="dateA - dateB, frequency; number of observations="+str(n)
        )
    })
    shutil.move("temp-plot.html",filename)

def plot_box(data,n,filename):
    plotly.offline.plot({
        "data":data
        ,"layout":Layout(
            title="dateA - dateB; number of observations="+str(n)
        )
    })
    shutil.move("temp-plot.html",filename)

def box_plot_all(date_ranges,date_types,filename):
    data = []
    dicter = {
        "dateA":'rgb(0, 0, 255)',
        "dateB":"rgb(255,0,0)",
        "dateC":"rgb(0,128,0)"
    }
    for ind,date_range in enumerate(date_ranges):
        data += prepare_for_box_plot(date_range,date_types[ind],dicter[date_types[ind]])
    n = len(data)
    date_type = "_".join(date_types)
    plotly.offline.plot({
        "data":data
        ,"layout":Layout(
            title="dateA - blue, dateB - red, dateC - green ; number of observations="+str(n)
        )
    })
    shutil.move("temp-plot.html",filename)

def plot_all_barchart(filename):
    dateA_total = len([b for b in One.query.all() if b.dateA])
    dateB_total = len([b for b in One.query.all() if b.dateB and b.dateB.year >= 2012])
    dateC_total = len([b for b in One.query.all() if b.dateC and b.dateC.year >= 2012])
    one_total = One.query.count()
    x_vals = ["total data","total dateA","total dateB","total dateC"]
    y_vals = [dateA_total,dateB_total,dateC_total,one_total]
    plotly.offline.plot({
        "data":[Bar(x=x_vals,y=y_vals)],
        "layout":Layout(
            title="Frequency analysis of missing data"
        )
    })
    shutil.move("temp-plot.html",filename)
    
def plot_all_timeseries(dates,date_types,filename):
    for_scatter = []
    for ind,val in enumerate(dates):
        timeseries = prepare_for_timeseries(val)
        x_vals = [elem[0] for elem in timeseries]
        y_vals = [elem[1] for elem in timeseries]
        for_scatter.append(Scatter(x=x_vals,y=y_vals,name=date_types[ind]))
    plotly.offline.plot({
        "data":for_scatter,
        "layout":Layout(
            title="Time Series analysis of dateA,dateB,dateC"
        )
    })
    shutil.move("temp-plot.html",filename)

def plot_weekly_timeseries_dateA_date(dates,filename):
    df = prepare_for_timeseries_weekly(dates)
    x_vals = [elem.to_datetime() for elem in df["to_order"]]
    y_vals = df["count"].values.tolist()
    plotly.offline.plot({
        "data":[Scatter(x=x_vals,y=y_vals,name="dateA date")],
        "layout":Layout(
            title="week over week Time Series analysis"
        )
    })
    shutil.move("temp-plot.html",filename)

def timeseries_plot(dates,date_type,filename):
    n = len(dates)
    dates.sort()
    timeseries = prepare_for_timeseries(dates)
    x_vals = [elem[0] for elem in timeseries]
    y_vals = [elem[1] for elem in timeseries]
    plotly.offline.plot({
        "data":[
            Scatter(x=x_vals,y=y_vals,name="form8")
            ]
        ,"layout":Layout(
          title=date_type+" per month over time; number of observations="+str(n)
            )
        })
    shutil.move("temp-plot.html",filename)

def do_differencing():
    timeseries = differencing()
    box_sizes = size_of_boxes(timeseries)
    bar_chart_plot(box_sizes)
    boxes = differencing_box_plot(timeseries,"dateA_minus_dateB","rgb(0,0,255)")
    plot_box(boxes,len(timeseries))


def plot_total_count_of_cases_week_over_week(start_date,filename):
    timeseries = [b.dateA for b in One.query.filter(Brieff.dateA>start_date).all()]
    df = prepare_for_timeseries_weekly(timeseries)
    x_vals = [elem.to_datetime() for elem in df["to_order"]]
    y_vals = df["count"].values.tolist()
    plotly.offline.plot({
        "data":[Scatter(x=x_vals,y=y_vals,name="dateA")],
        "layout":Layout(
            title="Month over Month for "+str(start_date)+" - "+str(max(timeseries)) 
        )
    })
    shutil.move("temp-plot.html",filename)

def prepare_for_linear_prediction(timeseries):
    series = [[],[]]
    df = pd.DataFrame()
    for i in range(len(timeseries[0])):
        df = df.append({"x":(timeseries[0][i] - min(timeseries[0])).days,"y":timeseries[1][i]},ignore_index=True)
    results = formula.ols(formula="y ~ x",data=df) 
    return results,df

def plot_linear_prediction(results,data,filename):
    x_transform = (add_month(data[0][-1]) - min(data[0])).days
    x_val = add_month(data[0][-1])
    prediction = results.params["x"]*x_transform+results.params["Intercept"]
    trace1 = Scatter(
        x=data[0], 
        y=data[1], 
        mode='lines',
        marker=Marker(color='rgb(255, 127, 14)'),
        name='Data'
    )

    trace2 = Scatter(
        x=[x_val], 
        y=[prediction], 
        mode='markers',
        marker=Marker(color='rgb(31, 119, 180)'),
        name='Fit'
    )

    layout = Layout(
        title='Linear Fit in Python',
        plot_bgcolor='rgb(229, 229, 229)',
        xaxis=XAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
        yaxis=YAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)')
    )

    to_scatter = [trace1,trace2]
    plotly.offline.plot({
        "data":to_scatter,
        "layout":layout
    })

    shutil.move("temp-plot.html",filename)
    
def plot_scatter_month_over_month(timeseries,filename):
    plotly.offline.plot({
        "data":[Scatter(x=timeseries[0],y=timeseries[1])],
        "layout":Layout(
            title="Total Count Month over Month for "+str(timeseries[0][0])+" - "+str(timeseries[0][-1])
            )
        })
    shutil.move("temp-plot.html",filename)


def plot_by_category(categories,total_count,filename):
    categories = order_dictionary(categories)
    x_vals = categories.keys()
    y_vals = [categories[elem] for elem in x_vals]
    plotly.offline.plot({
        "data":[Bar(x=x_vals,y=y_vals)],
        "layout":Layout(
            title="Frequency of categories number_obs="+str(total_count)
            )
        })
    shutil.move("temp-plot.html",filename)

def plot_by_categories_bar_with_mapping(mapping,categories,total_count,filename):
    categories = order_dictionary(categories)
    x_vals = [mapping[key] for key in categories.keys()]
    y_vals = [categories[key] for key in categories.keys()]
    plotly.offline.plot({
        "data":[Pie(x=x_vals,y=y_vals)],
        "layout":Layout(
            title="Categories with mappings"
            )
        })
    shutil.move("temp-plot.html",filename)


def plot_stacked_barchart(categories,start_date,end_date,filename):
    #{ key: [value1,value2, ..., valueN] }
    categories = OrderedDict(categories)
    category_names = list(categories.keys())
    category_names.sort()
    RO_x = category_names
    category_types = list(categories[category_names[0]].keys())
    data = [Bar(x=category_names,y=[categories[category] for category in category_names],name=category_type) for category_type in category_types]
    
    plotly.offline.plot({
        "data":data,
        "layout":Layout(
            title="Working Title",
            barmode="stack"
            )
        })
    shutil.move("temp-plot.html",filename)

def doing_prediction():
    results,df = prepare_for_prediction(timeseries)
    plot_linear_prediction(results.fit(),timeseries)
   
def count_from_db():
    count_per_instance = []
    grouping_of_instances = []
    keys = ["A","B","C"]
    for f in Two.query.all():
        tmp = {}.fromkeys(keys,0)
        counts = 0
        if f.A:
            counts += 1
            tmp["A"] += 1
        if f.B:
            counts +=1
            tmp["B"] += 1
        if f.C:
            counts +=1
            tmp["C"] += 1
        count_per_instance.append(counts)
        grouping_of_instances.append(tmp)
    return count_per_instance, grouping_of_instances

def describe_contentions(count_per_instance):
    _,_,mean,variance,skew,kurtosis = describe(sp.array(count_per_instance))
    return mean,variance, skew,kurtosis,len(count_per_instance),Two.query.count()

def get_groupings(grouping_of_instances):
    groupings = {}
    num_groupings = {}
    for grouping in grouping_of_instances:
        if sum(grouping.values()) > 1:
            group = ""
            for key in grouping.keys():
                if grouping[key] >= 1:
                    group += key + ", "
            group = group.strip()
            num_group = len(group.split(","))
            if not group in num_groupings.keys():
               num_groupings[group] = num_group
            try:
                groupings[group] += 1
            except:
                groupings[group] = 1
    return groupings, num_groupings

def groupings_bar_chart(groupings):
    x_vals = groupings.keys()
    y_vals = [groupings[key] for key in x_vals]
    plotly.offline.plot({
        "data":[Bar(x=x_vals,y=y_vals)],
        "layout":Layout(
            title="Grouping and Count"
            )
        })

    
def counts_bar_chart(count_per_instance):
    n = Two.query.count()
    count_freq = {}
    for count in count_per_instance:
        if count in count_freq.keys():
            count_freq[count] += 1
        else:
            count_freq[count] = 1
    
    x_vals = count_freq.keys()
    y_vals = [count_freq[key] for key in x_vals]
    x_vals = [num2words(1)+" count"] + [num2words(elem)+" count" for elem in x_vals if elem != 1]
    plotly.offline.plot({
        "data":[Bar(x=x_vals,y=y_vals)],
        "layout":Layout(
            title="Counts By Frequency"
            )
        })

    
def count_groupings_plots():
    count_per_instance,grouping_per_instances = count_from_db()
    groupings,num_groupings = get_groupings(grouping_per_instances)
    groupings_bar_chart(num_groupings)
    counts_bar_chart(count_per_instance)


def cur_age_shape_plot(ages,filename):
    plotly.offline.plot({
        "data":[Bar(x=ages,y=ages,text="ages")],
        "layout":Layout(
            title="Shape of age distribution"
            )
        })
    shutil.move("temp-plot.html",filename)

def cur_age_freq_plot(ages,number_of_observations,filename):
    plotly.offline.plot({
        "data":[Bar(x=["20-30","30-40","40-50","50-60","60-70","70-80","80-90","90-100"],y=ages,text="ages")],
        "layout":Layout(
            title="Frequencies of people by age segmentation number of observations="+str(number_of_observations)
            )
        })

    shutil.move("temp-plot.html",filename)

def segmentation_analysis(values,filename):
    data = [len(b) for b in segment_by_type(brieffs)]
    names =["type one","type two"]

    plotly.offline.plot({
        "data": [Bar(x=names,y=data)],
        "layout":Layout(
            title="Segmentation analysis"
        )
        })
    shutil.move("temp-plot.html",filename)

def timeseries_analysis(values,filename):    
    data = segment_by_type(values)
    texts = ["type_one","type_two"]
    names =["type_one","type_two"]

    for_scatter = []
    for ind,val in enumerate(texts):
        x_vals,y_vals = prepare_for_timeseries(data[ind])
        for_scatter.append(Scatter(x=x_vals,y=y_vals,name=names[ind],text=val))

    plotly.offline.plot({
        "data": for_scatter,
        "layout":Layout(
            title="Time Series analysis"
        )
        })
    shutil.move("temp-plot.html",filename)

   
def simple_plot_freq(category_key,x_vals,y_vals,filename):    
    plotly.offline.plot({
        "data":
        [Scatter(x=x_vals,y=y_vals,mode="markers")],
        
        "layout":
        Layout(
            title="By type for "+category_key
            )
        })
    category_key = category_key.replace(" ","_")
    category_key = category_key.split("_n=")[0].strip()
    shutil.move("temp-plot.html",filename)

def plot_level_freq(category,category_key):
    values,keys = impose_order(category)
    x_vals = keys
    y_vals = values
    very_low_frequency_categories = OrderedDict({})
    low_frequency_categories = OrderedDict({})
    mid_frequency_categories = OrderedDict({})
    high_frequency_categories = OrderedDict({})
    for ind,val in enumerate(y_vals):
        if val <= 10:
            if not val in very_low_frequency_categories.keys():
                very_low_frequency_categories[val] = [x_vals[ind]]
            else:
                very_low_frequency_categories[val].append(x_vals[ind])
        elif val > 10 and val <= 21:
            if not val in low_frequency_categories.keys():
                low_frequency_categories[val] = [x_vals[ind]]
            else:
                low_frequency_categories[val].append(x_vals[ind])
        elif val > 21 and val < 500:
            if not val in mid_frequency_categories.keys():
                mid_frequency_categories[val] = [x_vals[ind]]
            else:
                mid_frequency_categories[val].append(x_vals[ind])
        else:
            if not val in high_frequency_categories.keys():
                high_frequency_categories[val] = [x_vals[ind]]
            else:
                high_frequency_categories[val].append(x_vals[ind])
    very_low_x_vals = []
    very_low_y_vals = []
    low_x_vals = []
    low_y_vals = []
    mid_x_vals = []
    mid_y_vals = []
    high_x_vals = []
    high_y_vals = []
    
    for key in very_low_frequency_categories.keys():
        for value in very_low_frequency_categories[key]:
            very_low_x_vals.append(value)
            very_low_y_vals.append(key)
    for key in low_frequency_categories.keys():
        for value in low_frequency_categories[key]:
            low_x_vals.append(value)
            low_y_vals.append(key)
    for key in mid_frequency_categories.keys():
        for value in mid_frequency_categories[key]:
            mid_x_vals.append(value)
            mid_y_vals.append(key)
    for key in high_frequency_categories.keys():
        for value in high_frequency_categories[key]:
            high_x_vals.append(value)
            high_y_vals.append(key)

    # print "very low x vals"
    # print very_low_x_vals
    # print
    # print "very low y vals"
    # print very_low_y_vals
    # print
    simple_plot_freq("Very Low Frequency n="+str(len(very_low_x_vals)),very_low_x_vals,very_low_y_vals)
    simple_plot_freq("Low Frequency n="+str(len(low_x_vals)),low_x_vals,low_y_vals)
    simple_plot_freq("Mid Frequency n="+str(len(mid_x_vals)),mid_x_vals,mid_y_vals)
    simple_plot_freq("High Frequency n="+str(len(high_x_vals)),high_x_vals,high_y_vals)
