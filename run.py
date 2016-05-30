from helpers import *
from plots import *

def do_differencing():
    timeseries = differencing()
    box_sizes = size_of_boxes(timeseries)
    bar_chart_plot(box_sizes)
    boxes = differencing_box_plot(timeseries,"dateA_minus_dateB","rgb(0,0,255)")
    plot_box(boxes,len(timeseries))

def doing_prediction():
    results,df = prepare_for_prediction(timeseries)
    plot_linear_prediction(results.fit(),timeseries)
