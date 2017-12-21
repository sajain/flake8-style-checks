from setuptools import setup

install_requires = ['flake8>=1.5']

test_requires = ['flake8>=1.5']

setup(
    name='flake8-try-except',
    version='0.0.1',
    description='Uninitialized variable checker in try/except clauses',
    keywords='flake8 Try Except Uninitialized Variables',
    author='Saurabh Jain',
    author_email='jain.saurabhj@gmail.com',
    py_modules=['checker'],
    zip_safe=False,
    entry_points={
        'flake8.extension': [
            'S = try_except_checker:TryExceptUninitializedVariableChecker',
        ],
    },
    install_requires=install_requires,
    tests_require=test_requires,
    setup_requires=[],
    test_suite="nose.collector",
)
