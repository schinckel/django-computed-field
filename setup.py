from setuptools import find_packages, setup

setup(
    name='django-computed-field',
    version='0.1.0',
    description='ComputedField(): automatically annotate expressions',
    url='https://bitbucket.org/schinckel/django-computed-field',
    author='Matthew Schinckel',
    author_email='matt@schinckel.net',
    packages=find_packages('src', exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={},
    python_requires='>=3.6',
    install_requires=[
        'django'
    ],
    setup_requires=["pytest-runner", ],
    tests_require=["pytest", ],
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
