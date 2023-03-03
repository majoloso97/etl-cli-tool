# NS Data Engineer Assessment
Data Engineer Assessment project for NicaSource: Highly flexible ETL CLI tool to save data from CSV into MySQL

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/) [![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/) [![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://www.github.com/) 

## Project description
This project consists in a CLI tool that runs a data pipeline designed to import Superstore Sales data from a CSV file into a MySQL database where the data would persist. 

The dataset for setting up schemas was taken from [Kaggle](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting). A first exploration phase was done to check the shape of the data and needed transformations (see `data_exploration.ipynb` file in the repository).

The project is structured as a Python package intended for local use, and not intended for public use. This decision was made under the consideration that the tool would be used by the author (me) and potential team members under a controlled environment such as local development, connected to a remote database, production servers that would need to carry on the ELT tasks periodically or on other systems we might have control of. 


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

## Running the project
The following steps show how this CLI should be installed and used for testing the functionality locally, or even for production use.
### Tools for local testing
To simulate a production environment, a `docker-compose` file was provided to start a MySQL instance locally. In case you already have a MySQL server, you can ignore this step.

The `docker-compose` makes sure that a database is available to simulate the loading phase of the ETL process, and sets up default permissions that are also used by the CLI tool when installed. Follow these steps to build the docker image:

- Make sure to have Docker and docker-compose installed and running on your computer. If you don't, you can install it from the [official site](https://www.docker.com/products/docker-desktop/) and launch Docker Destkop.
- Open a new terminal and cd to the repository folder in your machine.  
- In the terminal, run `docker-compose up --build`. This will create an image for the project, and also the database image. 
- To test if the database is running, you can use the following credentials using a database management tool like MySQL Workbench:
    - Username: `user`
    - Password: `admin`
    - Host: `127.0.0.1`
    - Port: `3306`
    - Database name: `etl_db`
### CLI Usage
Once installed, the ETL CLI tool can be used from a terminal by invoking the `etl` command. General information of the tool and the commands can be obtained by running `etl -h`.

From the help command, you can see the tool has three commands. you can access the help information from any of them by adding the -h flag when running the command:
- `etl show`: Show the current settings of the tool
- `etl config`: Adjust the tool settings
- `etl run`: Runs the ETL with data from the provided source

## Author
**Marvin López Osorio**

Python developer, Data enthusiast

[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:majoloso97@gmail.com) [![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/marvin-l%C3%B3pez-osorio-a723336a/) [![Instagram](https://img.shields.io/badge/Instagram-%23E4405F.svg?style=for-the-badge&logo=Instagram&logoColor=white)](https://www.instagram.com/marvinlopez97/)