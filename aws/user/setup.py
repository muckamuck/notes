from setuptools import setup
setup(
        name="AWSKeyTool",
        version='0.0.1',
        packages=['awskeytool'],
        description='Junk Drawer for AWS Key Utilities',
        author='Chuck Muckamuck',
        author_email='Chuck.Muckamuck@gmail.com',
        install_requires=[
                    "boto3>=1.7",
                    "Click>=6.7",
                    "pymongo>=3.6"
                ],
        entry_points="""
            [console_scripts]
            awskeytool=awskeytool.command:cli
        """
)
