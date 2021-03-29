import sys
sys.path.append(".")

from reportipy import Report
import matplotlib.pyplot as plt
import numpy as np


# TODO: Automate testing

def main():
    r = Report()
    r.add_section("Section")

    test_fig, ax = plt.subplots()

    ax.plot(np.arange(10), np.arange(10), "r", "-")

    r.add_figure(test_fig, "An upward line", width=r"0.5\textwidth")

    r.build("test.pdf")


main()
