from setuptools import Extension
from setuptools import setup

from setuptools_zig import BuildExt


setup(
    name="ex19",
    version="0.0.1",
    python_requires=">=3.7.15",
    cmdclass = {'build_ext': BuildExt},
    ext_modules=[
        Extension("ex19", ["src/ex19.zig"])
    ],
    setup_requires=['wheel'],
)
