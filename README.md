# Reportipy

So you are working on some machine learning model and create a whole lot of graphs and visualizations in your notebook. Later, you try some new parameters and get a new model that might be even better! So you fire up the notebook again, recreate the visualizations with your new fancy model and you think: "maybe this one graph was better in the previous version". But you already overwrote that file when evaluating your new model...

This package allows you to easily embed a set of matplotlib figures in a pdf file, to which you can refer to later on. No keeping several almost-identical notebooks around.

## Usage

To create a document, just use the `Report` class.

```python
from reportipy import Report

r = Report(title="My amazing figure")
# create a figure with matplotlib

# Add the figure, you can add as many as you would like
r.add_figure(plt.gcf(), caption="This is great stuff")

# Build the file
r.build("my_report.pdf")
```

## Dependencies

This package uses pdflatex to compile your document, so you have to have this installed.
