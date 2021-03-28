import tempfile
from subprocess import run
import shutil
from pathlib import Path

header = r"""
\documentclass{{article}}
\usepackage{{graphicx}}
\usepackage[margin=0.5in]{{geometry}}

\title{{ {title} }}

\begin{{document}}
\maketitle

{body}

\end{{document}}
"""

figtemplate = r"""
\begin{{figure}}[h]
    \centering
    \includegraphics[width={width}]{{{fn}}}
    \caption{{ {caption}  }}
\end{{figure}}
"""


class Report:
    def __init__(self, title="Title test"):
        self._docdir = tempfile.TemporaryDirectory()
        self.docdir = Path(self._docdir.name)
        self.maintex = self.docdir / "main.tex"
        self.figidx = 0
        self.body = ""
        self.title = title

    def add_body(self, string):
        self.body += string

    def add_section(self, title):
        """ Adds a new section to the document

        Argument:
            title: name of the new section
        """
        tex = r"\section{{{}}}\n".format(title)
        self.add_body(tex)

    def add_figure(self, fig, caption, width=r"\textwidth"):
        """ Adds a pyplot figure to the document

        Arguments:
            fig: pyplot figure handle
            caption: caption to add to the figure in the document
            width: the width of the image, by default this is set to the pagewidth
        """
        figfn = self.docdir / "{}.png".format(self.figidx)

        fig.tight_layout()
        fig.savefig(figfn, dpi=120)
        self.figidx += 1

        figtex = figtemplate.format(fn=str(figfn), caption=caption, width=width)
        self.add_body(figtex)

    def write_tex(self, fn=None):
        if not fn:
            fn = self.maintex

        buffer = header.format(title=self.title, body=self.body)

        with open(fn, "w") as f:
            f.write(buffer)

    def compile_tex(self):
        cmd = ["pdflatex", "-interaction", "nonstopmode", str(self.maintex)]

        run(cmd, cwd=self.docdir)
        run(cmd, cwd=self.docdir)

    def build(self, fn_out):
        self.write_tex()
        self.compile_tex()

        mainpdf = self.docdir / self.maintex.name.replace("tex", "pdf")
        shutil.copy(mainpdf, fn_out)

    def __del__(self):
        self._docdir.cleanup()
