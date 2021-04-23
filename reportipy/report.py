import tempfile
from subprocess import run
import shutil
from pathlib import Path
import matplotlib.pyplot as plt
from typing import Optional

header = r"""
\documentclass{{article}}
\usepackage{{graphicx}}
\usepackage[section]{{placeins}}
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
    \caption{{{caption}}}
\end{{figure}}
"""


class Report:
    """This object keep track of the necessary information to create small report documents using a LaTeX template.
    Files (such as figures, images, tex code,...) are stored in a temporary directory that is automatically cleaned up
    when this object is destroyed.
    """

    def __init__(self, title: str = "Title test"):
        self._docdir = tempfile.TemporaryDirectory()
        self.docdir = Path(self._docdir.name)
        self.maintex = self.docdir / "main.tex"
        self.figidx = 0
        self.body = ""
        self.title = title

    def add_body(self, string: str):
        self.body += string

    def add_section(self, title: str):
        """Adds a new section to the document

        Argument:
            title: name of the new section
        """
        tex = r"\section{{{}}}".format(title) + "\n\n"
        self.add_body(tex)

    def add_subsection(self, title: str):
        """Adds a new subsection to the document

        Argument:
            title: name of the new subsection
        """
        tex = r"\subsection{{{}}}".format(title) + "\n\n"
        self.add_body(tex)

    def add_figure(self, fig: plt.Figure, caption: str, width: str = r"\textwidth"):
        """Adds a pyplot figure to the document

        Arguments:
            fig: pyplot figure handle
            caption: caption to add to the figure in the document
            width: the width of the image, by default this is set to the pagewidth
        """
        figfn = self.docdir / "{}.png".format(self.figidx)

        fig.tight_layout()
        fig.savefig(figfn, dpi=120)
        self.figidx += 1

        figtex = figtemplate.format(fn=figfn.name, caption=caption, width=width)
        self.add_body(figtex)

    def _write_tex(self, fn: Optional[Path] = None):
        """Write the tex document to the temp directory"""
        if not fn:
            fn = self.maintex

        buffer = header.format(title=self.title, body=self.body)

        with open(fn, "w") as f:
            f.write(buffer)

    def _compile_tex(self):
        """Run pdflatex to create the document."""
        cmd = ["pdflatex", "-interaction", "nonstopmode", str(self.maintex)]

        run(cmd, cwd=self.docdir)
        run(cmd, cwd=self.docdir)

    def build(self, fn_out: Path):
        """Create the document by compiling tex code with pdflatex. The resulting document is copied from the temporary
        directory to the desired output destination.

        Arguments:
            fn_out: output path for the report
        """
        self._write_tex()
        self._compile_tex()

        mainpdf = self.docdir / self.maintex.name.replace("tex", "pdf")
        shutil.copy(mainpdf, fn_out)

    def __del__(self):
        self._docdir.cleanup()
