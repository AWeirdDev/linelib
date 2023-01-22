from distutils.core import setup

setup(
    name='linelib',
    version='2',
    packages=['linelib', 'linelib.notify', 'linelib.ext', 'linelib.connect', 'linelib.model'],
    license='MIT',
    description="The solution to simplicity.",
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    author='AWeirdScratcher',
    author_email = "aweirdscrather@gmail.com",
    install_requires=[
        'httpx', 'urllib3', 'flask', 'flask-cors', 'termcolor'
    ],
    keywords = ['line', 'bot', 'line bot', 'sdk'],
    url="https://github.com/AWeirdScratcher/linelib",
    classifiers=[
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.10'
  ]
)