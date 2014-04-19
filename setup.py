#!/usr/bin/env python
#encoding: utf-8
"""
setup.py file for pylibgadu project
"""

from distutils.core import setup, Extension


libgadu_module = Extension('_libgadu',
                           sources=['libgadu_wrap.c'],
                           libraries=['gadu']
                           )
setup(name='libgadu',
       version='1.11.3',
       author=u"Michał Papierski",
       author_email='michal@papierski.net',
       description="""Python libgadu wrapper""",
       ext_modules=[libgadu_module],
       py_modules=["libgadu"],
       )