import os
from setuptools import setup, find_packages

VERSION = '0.1.1'
INSTALL_REQUIRES = [
    'setuptools',
    'esculator',
    'openprocurement.auction',
    'openprocurement.auction.worker'
]
EXTRAS_REQUIRE = {
    'test': [
        'pytest',
        'pytest-cov'
    ]
}
ENTRY_POINTS = {
    'console_scripts': [
        'auction_esco = openprocurement.auction.esco.cli:main',
    ],
    'openprocurement.auction.auctions': [
        'esco = openprocurement.auction.esco.includeme:includeme'
    ],
    'openprocurement.auction.robottests': [
        'esco_tests = openprocurement.auction.esco.tests.functional.main:includeme'
    ]
}

setup(name='openprocurement.auction.esco',
      version=VERSION,
      description="",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
      ],
      keywords='',
      author='Quintagroup, Ltd.',
      author_email='info@quintagroup.com',
      license='Apache License 2.0',
      url='https://github.com/ProzorroUKR/openprocurement.auction.esco',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['openprocurement', 'openprocurement.auction'],
      include_package_data=True,
      zip_safe=False,
      install_requires=INSTALL_REQUIRES,
      extras_require=EXTRAS_REQUIRE,
      entry_points=ENTRY_POINTS
      )
