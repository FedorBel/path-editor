from distutils.core import setup, Extension

module1 = Extension("fooMod", sources=["hack.c"])

setup(
    name="fooMod",
    version="1.0",
    description="This is a demo package",
    ext_modules=[module1],
)
