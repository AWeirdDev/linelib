from distutils.core import setup

setup(
    name='linelib',
    version='0.1',
    packages=['linelib', 'linelib.http', 'linelib.models'],
    license='MIT',
    description="Launch your LINE bot to the next level.",
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    author='AWeirdScratcher',
    author_email = "aweirdscrather@gmail.com",
    install_requires=[
        'requests', 'flask'
    ],
    keywords = ['line', 'bot', 'line bot', 'sdk'],
    url="https://github.com/AWeirdScratcher/linelib"
)
