from setuptools import setup

setup(
    name="reportipy",
    version="0.0.1",
    author="Tom Roussel",
    author_email="tom.roussel85@gmail.com",
    packages=["reportipy"],
    description="Easily generate pdf's containing a collection of images. For example, useful to package visualizations of machine learning models.",
    install_requires=[
        "matplotlib"
    ]
)


