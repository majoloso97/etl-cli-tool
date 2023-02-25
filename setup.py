from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

with open("requirements.txt", "r", encoding="utf-8") as reqs:
    requirements = reqs.read()
    
setup(
    name = 'ns_data_eng_assessment_mjlo',
    version = '0.0.1',
    author = 'Marvin López Osorio',
    author_email = 'majoloso97@gmail.com',
    description = 'Data Engineer Assessment project for NicaSource',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/majoloso97/ns-data-engineer-assessment',
    py_modules = ['cli', 'src'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.9',
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        etl=cli:cli
    '''
)