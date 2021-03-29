import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[2]))

from reportipy import Report
import matplotlib.pyplot as plt
import numpy as np
import unittest
import re


class ReportTest(unittest.TestCase):
    def setUp(self):
        self.report = Report("DocumentName")

    def test_compile(self):
        pass

    def test_title(self):
        self.report._write_tex()
        tex = self.tex_contents()
        pattern = r"^\\title{ DocumentName }"
        match = re.search(pattern, tex, flags=re.MULTILINE)
        if not match:
            raise ValueError("Pattern '{}' not found".format(pattern))

    def test_figure(self):
        test_fig, ax = plt.subplots()
        ax.plot(np.arange(10), np.arange(10), "r", "-")
        self.report.add_figure(test_fig, "An upward line", width=r"0.5\textwidth")

        assert (self.report.docdir / "0.png").exists(), "Figure was not written to disk"
        self.report._write_tex()

        tex = self.tex_contents()
        pattern_graph = r"\\includegraphics\[width=0.5\\textwidth\]{0.png}"
        match = re.search(pattern_graph, tex, flags=re.MULTILINE)
        print(tex)
        assert match, "Figure not in tex code"

        pattern_graph = r"\\caption{An upward line}"
        match = re.search(pattern_graph, tex, flags=re.MULTILINE)
        assert match, "Figure caption is wrong"


    def test_section(self):
        self.report.add_section("SectionTest")
        self.report._write_tex()
        tex = self.tex_contents()

        pattern = r"\\section{SectionTest}"
        match = re.search(pattern, tex, flags=re.MULTILINE)

        print(tex)
        assert match, "Section is not found in the tex file "

    def tex_contents(self):
        with open(self.report.maintex) as f:
            return f.read()



def main():
    r = Report()
    r.add_section("Section")

    test_fig, ax = plt.subplots()

    ax.plot(np.arange(10), np.arange(10), "r", "-")

    r.add_figure(test_fig, "An upward line", width=r"0.5\textwidth")

    r.build("test.pdf")


main()
