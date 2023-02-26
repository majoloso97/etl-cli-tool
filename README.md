# NS Data Engineer Assessment
Data Engineer Assessment project for NicaSource: Highly flexible ETL CLI tool to save data from CSV into MySQL

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/) [![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/) [![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://www.github.com/) 

## Project description
This project consists in a CLI tool that runs a data pipeline designed to import Car Sales data from a CSV file into a MySQL database where the data would persist. 

The project is structured as a Python package intended for local use, and not intened for public use. This decision was made under the consideration that the tool would be used by the author (me) and potential team members under a controlled environment such as local development, connected to a remote database, production servers that would need to carry on the ELT tasks periodically or on other systems we might have control of. 


## Project structure
### Considerations
- The tool is going to be installed as a local package.
- There is just a single data storage, which will have a particular table for the processed data.
- Though the core functionality is highly flexible, the CLI options just allow to have a basic interaction with the tool. More customization could be added as needed.
- Basic configurations can be set up from the CLI (like how to show/store the logs, or how the database credentials will be provided). See **CLI usage** for more details.

### Overall design
This application logic of the project is divided according to the logical steps of the ETL process. Thus, we have pieces of code dedicated to Extracting data, Transforming it and then Loading it to the final storage location, in this case, a MySQL database. 

- Extraction: A Factory Design Pattern was used with a base AbstractExtractor class containing two main functions: import_data and verify_origin (plus other miscellaneous like logging and column verification). The purpose of the children of this class is to ingest the data from potentially different sources, and ensure the schema of the incoming data matches the expected data (from the example input file). The Extractor classes also should always be able to provide a unified data output in the form of pandas dataframe, to be part of a pipeline.

- Transformation: The Functional Pipeline Pattern was chosen for this section. There are several independent functions that transform dataframes, all sharing the characteristic of accepting and returning dataframes as inputs/outputs. More functions can be added to the transformers directory as needed with the only restriction of having this unified input/output design. A global generic Pipeline class was built to apply these transformations (read more below).

- Loading: There is just one Loader class in all the project because the requirements ask for flexibility in the Extration and Transformation phases. However, they don't ask for support of different data repositories or strategies.

- Pipeline: The Pipeline class not only applies transformations. It was  built to manage the complete ETL process. Thus, it uses the Extractor classes to get data, apply the Transformer functions (that can be ensembled in different fashions as needed) to the data, and load it to the database using the Loader class.

## Author
**Marvin López Osorio**

Python developer, Data enthusiast

[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:majoloso97@gmail.com) [![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/marvin-l%C3%B3pez-osorio-a723336a/) [![Instagram](https://img.shields.io/badge/Instagram-%23E4405F.svg?style=for-the-badge&logo=Instagram&logoColor=white)](https://www.instagram.com/marvinlopez97/)