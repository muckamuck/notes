from setuptools import setup
setup(
    name="fix_util",
    version='0.0.1',
    packages=['fix_util'],
    description='Fix a directory with jacked up names',
    author='Chuck Muckamuck',
    author_email='chuck.muckamuck@gmail.com',
    install_requires=[
        "Click>=6.7"
    ],
    entry_points="""
        [console_scripts]
        fix_util=fix_util.command:cli
    """
)
