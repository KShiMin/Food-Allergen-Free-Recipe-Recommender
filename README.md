# 🥗 Food Allergen Free Recipe Recommender
The Food Allergen Free Recipe Recommender is a tailored recipe application designed to provide safe, personalised, and delicious recipes for individuals with food allergies or dietary restrictions.

## 📋 Prerequisites
Before you begin, ensure you have the following installed on your system:

- **Python 3.10 or newer**
- **MongoDB** installed and running locally (default port: `27017`)
- **uv** package manager

If you do not have `uv` installed, you can install it using pip:

```bash
pip install uv
```

## Setup Guide
### Virtual Environment
Set up a Virtual Environment using:
```bash
uv venv
```
### Install Dependencies
```bash
uv pip install .
```

### 🗄️ Populating noSQL Database (ETL)
Before starting the application, you must populate the NoSQL data.
<b>Make sure your database server is running and configured correctly before executing this step.</b>

Run the ETL script:
```bash
uv run etl
```

This script will:

* Extract data from the source files
* Transform the data as needed
* Load the data into your NoSQL database


### 🌐 Running the Web Application
After the ETL step completes successfully, you can start the web application:

```bash
uv run ui
```
This starts the web interface, where you can:

- Select your allergens
- Browse safe recipes
- View alternative ingredient recommendations
