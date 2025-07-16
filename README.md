# Food-Allergen-Free-Recipe-Recommender
SIT INF2003 Database System Project. This project, Food Allergen Free Recipe Recommender, is a tailored recipe application designed to provide safe, personalised and delicious recipes that take into account individuals with any food allergies or dietary restrictions.

# 📗 Allergen-Free Recipes System

This project provides a complete recipe management system, including:
- ETL pipeline to populate recipe and review data into MongoDB.
- Web user interface to browse and manage recipes.

---

## 🟢 Prerequisites

- **Python 3.10 or newer**
- **MongoDB** installed and running locally (default port: `27017`)
- **uv** package manager

If you do not have `uv` installed, you can install it using pip:

```bash
pip install uv
```

### Setup Guide
## Dependencies Installation
```bash
uv pip install .
```

### 📂 Populating the Database (ETL)
Before starting the application, you must populate the NoSQL data.

Run the ETL script:
```bash
uv run etl
```

This script will:

* Extract data from the source files
* Transform the data as needed
* Load the data into your NoSQL database

Make sure your database server is running and configured correctly before executing this step.

### 🌐 Running the Web Application
After the ETL step completes successfully, you can start the web application:

```bash
uv run ui
```
