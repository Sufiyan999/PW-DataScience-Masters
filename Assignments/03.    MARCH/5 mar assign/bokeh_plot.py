from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider
import numpy as np

# Prepare data and create a ColumnDataSource
x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]
y = np.exp(x)
source = ColumnDataSource(data={'x': x, 'y': y})

# Create a figure and add glyphs
plot = figure(title="Real-Time Plot")
plot.line('x', 'y', source=source, line_width=2)

# Create an interactive slider widget
slider = Slider(start=0, end=10, value=5, step=1, title="Shift Y-values")

# Define callback function
def update_data(attrname, old, new):
    shift = slider.value
    new_y = [val + shift for val in y]
    source.data = {'x': x, 'y': new_y}

# Connect slider widget to callback function
slider.on_change('value', update_data)

# Add widgets and plot to document
curdoc().add_root(plot)
curdoc().add_root(slider)
