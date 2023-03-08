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

- Loading: There is just one Loader class in all the project because the requirements ask for flexibility in the Extration and Transformation phases, but not for support of different data repositories or strategies. However, it's possible to extend this functionality with the same factory design used in the Extractor classes.

- Pipeline: The Pipeline class not only applies transformations. It was  built to manage the complete ETL process. Thus, it uses the Extractor classes to get data, apply the Transformer functions (that can be ensembled in different fashions as needed) to the data, and load it to the database using the Loader class. A worker function is provided, which purpose is to run the actual Pipeline methods, and pass the required transformations. Different sets of extractors or transformations could be used within the worker to solve different tasks.

## Running the project
The following steps show how this CLI should be installed and used for testing the functionality locally, or even for production use.
### Installation
This CLI is intended to be used as a local package. Thus it has to be installed with the local code pulled from the repository. Follow these steps to install the tool:
- Make sure to have Python (version>=3.7) and pip package manager installed on your computer. If you don't, you can install it from the [official site](https://www.python.org/).
- Make sure you have git installed on your system, or get it from the [official site](https://git-scm.com/downloads).
- Run `git clone https://github.com/majoloso97/ns-data-engineer-assessment.git` to get a local copy of the repository.
- Open a terminal and cd to the folder containing the cloned repository. Once there, run `pip install -e .` (include the dot at the end) so the package gets installed in development mode.
- Note: for production use you can instead run `pip install 'ns_data_eng_assessment_mjlo @ git+https://github.com/majoloso97/ns-data-engineer-assessment'` to install the package from the remote repository directly without manually cloning from github.
### Tools for local testing
Before using the CLI it's important to have a target database to run the pipeline. To simulate a production environment, a `docker-compose` file was provided to start a MySQL instance locally. In case you already have a MySQL server, you can ignore this step.

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
- `etl show -h`: Show the current settings of the tool
- `etl config -h`: Adjust the tool settings
- `etl run -h`: Runs the ETL with data from the provided source


#### **Showing current configuration**
Run `etl show`. It'll return the current settings of the tool, for example: 
```
>>> etl show
[2023-03-09 00:09:15,753] CLI SHOW | INFO: Current log-type set to Console [C]
[2023-03-09 00:09:15,789] CLI SHOW | INFO: Current db-auth set to Environment variables [E]
```
#### **Changing CLI configuration**
Run `etl config` to adjust settings for the CLI tool, such as: 
- Log type: with the flag `--log-type`, the type of logs output can be chosen between Console (value `c`, `C`)for terminal output, Logfile (`l`, `L`) for saving in .log file in the directory where the tool is run from, and Database (`d`, `D`) for saving directly in the same database where the processed data will be loaded (a table called `etl_logs`). Even when choosing Logfile or Database output, the logs will be shown in the terminal too.
- Source of database authentication details: with the flag `--db-auth`, you can choose to search for database authentication details (host, port, username, password, database name) in Environment variables (value `e`, `E`) to look for said details in global environment variables, or Prompt (`p`, `P`) to ask the user for the auth details. 

Once caught, these details are saved for future use, so you won't be asked again (nor the tool will try to get the data from env) until you run the `config` command again. 

Please note that when installed, the CLI has a configuration equivalent to `--log-type C`, so it will just output logs to terminal. Also the default database authorization details are set up to generic values to be able to test the CLI with the MySQL instance built by the provided `docker-compose`. If you want to use custom values, it's recommended to run `etl config --db-auth P` and input the details accordingly.

If the provided details are not valid, an error will be prompted in the terminal logs.

Use examples: 
- `etl config --log-type L --db-auth E`: Set up logs to be saved in .log file and database authentication to be gotten from environment.
- `etl config --log-type D`: Change the log output to database. The `--db-auth` parameter is not changed.
- `etl config --db-auth P`: Asks the user for database authentication details, the `--log-type` parameter remains unchanged.

An example from the terminal:

```
>>> etl config --log-type L --db-auth E
[2023-03-09 00:32:28,324] CLI CONFIG | INFO: Log type set to Logfile [L].
[2023-03-09 00:32:28,345] CLI CONFIG | INFO: Db Auth set to Environment variables [E].
```

#### **Running ETL process**
The command `etl run` allows to execute the Pipeline and the actual ETL process. It has an optional parameter `-o` to select an origin type. There is only one origin allowed at the moment (CSV files), so this parameter defaults to csv.

The FILEPATH parameter is required, and it should be a valid path to the csv file that needs processing. The tool will evaluate the schema as part of the pipeline and will reject files with missing columns. For testing purposes, you can use the `train.csv` file stored in the repository.

The following examples are equivalent:
- `etl run -o csv train.csv`
- `etl run train.csv`

A successful execution will look like:
```
>>> etl run train.csv
[2023-03-09 00:35:47,792] CLI START | INFO: Connection with database established.
[2023-03-09 00:35:47,793] PIPELINE | INFO: Starting extraction process
[2023-03-09 00:35:47,793] EXTRACT | INFO: The data source train3.csv was verified as a CSV file
[2023-03-09 00:35:47,793] EXTRACT | INFO: Extracting data from train3.csv
[2023-03-09 00:35:47,841] EXTRACT | WARNING: Excedent columns in origin file against expected schema. Dropping excedent columns.
[2023-03-09 00:35:47,842] PIPELINE | INFO: Starting to apply defined transformations
[2023-03-09 00:35:47,842] TRANSFORM | INFO: Renaming columns
[2023-03-09 00:35:47,843] TRANSFORM | INFO: Removing unnecessary columns (Row ID)
[2023-03-09 00:35:47,846] TRANSFORM | INFO: Input data contains 9800 rows. Looking for rows with missing values
[2023-03-09 00:35:47,857] TRANSFORM | WARNING: Found and dropped 11 rows. Continuing with 9789 valid rows.
[2023-03-09 00:35:47,857] TRANSFORM | INFO: Changing type of order_date, ship_date to datetime.
[2023-03-09 00:35:47,866] TRANSFORM | INFO: Getting Year out of order_date, ship_date columns.
[2023-03-09 00:35:47,868] TRANSFORM | INFO: Encoding country, segment, category, ship_mode, region columns to numbers.
[2023-03-09 00:35:48,607] PIPELINE | INFO: Starting to load data to database
[2023-03-09 00:35:48,607] LOAD | INFO: Starting connection to Database
[2023-03-09 00:35:48,633] LOAD | INFO: Bulk saving data
[2023-03-09 00:35:49,734] LOAD | INFO: Save transaction is completed
[2023-03-09 00:35:49,734] PIPELINE | INFO: ETL ran sucessfully
```

Any errors encountered during the Pipeline execution will be shown in the terminal logs, for example:
```
>>> etl run train2.csv
[2023-03-09 00:36:52,524] CLI START | INFO: Connection with database established.
[2023-03-09 00:36:52,525] PIPELINE | INFO: Starting extraction process
[2023-03-09 00:36:52,525] EXTRACT | INFO: The data source train2.csv was verified as a CSV file
[2023-03-09 00:36:52,525] EXTRACT | INFO: Extracting data from train2.csv
[2023-03-09 00:36:52,564] EXTRACT | ERROR: Missing columns in origin file against expected schema. Cannot proceed extraction.
[2023-03-09 00:36:52,564] PIPELINE | CRITICAL: ETL can't extract data. Check previous logs for information
```
## Author
**Marvin López Osorio**

Python developer, Data enthusiast

[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:majoloso97@gmail.com) [![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/marvin-l%C3%B3pez-osorio-a723336a/) [![Instagram](https://img.shields.io/badge/Instagram-%23E4405F.svg?style=for-the-badge&logo=Instagram&logoColor=white)](https://www.instagram.com/marvinlopez97/)