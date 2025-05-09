### Project Overview: Airflow TLS Pipeline with Postgres and API Integration
This project involves creating an ETL (Extract, Transform, Load) pipeline using Apache Airflow. The pipeline extracts data from an external API (in this case, NASA's Astronomy Picture of the Day (APOD) API), transforms the data, and loads it into a Postgres database. The entire workflow is orchestrated by Airflow, a platform that allows scheduling, monitoring, and managing workflow.

The project leverages Docker to run Airflow and Postgres as services, ensuring an isolated and reproducible environment. We also utilize Airflow hooks and operators to handle the ETL process efficiently.

### 📸 Screenshots & Demo

This section presents screenshots from the deployed ETL pipeline built with Apache Airflow and connected to a managed PostgreSQL instance on AWS (RDS).  
All screenshots are stored in the `screens/` folder.

---

#### 🛰️ DAG Overview  
**File:** `screens/Screenshot 2025-05-09 at 16.37.38.png`

![DAG Overview](screens/Screenshot%202025-05-09%20at%2016.37.38.png)

Airflow DAG run view showing all tasks (`create_table`, `extract_apod`, `transform_apod_data`, `load_data_to_postgres`) completed successfully. Execution time and task statuses are visible.

---

#### 📆 DAG Trigger & Schedule  
**File:** `screens/Screenshot 2025-05-09 at 16.37.54.png`

![DAG List](screens/Screenshot%202025-05-09%20at%2016.37.54.png)

Airflow main DAG dashboard. The `nasa_apod_postgres` DAG is enabled, scheduled daily (`0 0 * * *`), and the last run succeeded.

---

#### 🔗 DAG Dependency Graph  
**File:** `screens/Screenshot 2025-05-09 at 16.38.22.png`

![DAG Graph](screens/Screenshot%202025-05-09%20at%2016.38.22.png)

Visual graph of task dependencies inside the DAG. Shows task flow: `create_table` → `extract_apod` → `transform_apod_data` → `load_data_to_postgres`.

---

#### 🧮 PostgreSQL Query in DBeaver  
**File:** `screens/Screenshot 2025-05-09 at 16.38.49.png`

![DBeaver](screens/Screenshot%202025-05-09%20at%2016.38.49.png)

Shows a query on AWS RDS PostgreSQL using DBeaver. The `apod_data` table contains the latest data from the NASA API.

---

#### 🌌 APOD Image Preview  
**File:** `screens/Screenshot 2025-05-09 at 16.39.04.png`

![NASA Image](screens/Screenshot%202025-05-09%20at%2016.39.04.png)

Image of the Astronomy Picture of the Day, retrieved from the NASA API and stored via the pipeline.

---

#### 🛠️ AWS RDS Console  
**File:** `screens/Screenshot 2025-05-09 at 16.43.47.png`

![RDS Console](screens/Screenshot%202025-05-09%20at%2016.43.47.png)

Screenshot from the AWS Console confirming that the Postgres database instance (`db.t4g.micro`) is up and running in the Stockholm (eu-north-1) region.

### Key Components of the Project:

#### Airflow for Orchestration:  

Airflow is used to define, schedule, and monitor the entire ETL pipeline. It manages task dependencies, ensuring that the process runs sequentially and reliably. The Airflow DAG (Directed Acyclic Graph) defines the workflow, which includes tasks like data extraction, transformation, and loading. 

#### Postgres Database:

A PostgreSQL database is used to store the extracted and transformed data. Postgres is hosted in a Docker container, making it easy to manage and ensuring data persistance through Docker volumes. We interact with Postgres using Airflow's PostgresHook and PostgresOperator. 

#### NASA API (Astronomy Picture of the Day):

The external API used in this project is NASA's APOD API, which provides data about the atronomy picture of the day, including metadata like the title, explanation, and the URL of the image. We use Airflow's SimpleHttpOperator to extract data from the API. 

### Objectives of the Project:

#### Extract Data:

The pipeline extracts astronomy-related data from NASA's APOD API on a scheduled basis (daily, in this case). 

#### Transform Data:

Transformations such as filtering or processing the API response are performed to ensure that the data is in a suitable format before being inserted into the database.

#### Load Data into Postgres:

The transformed data is loaded into a Postgres database. The data can be used for further analysis, reporting, or visualization.

### Architecture and Workflow: 

The ETL pipeline is orchestrated in Airflow using DAG (Directed Acyclic Graph). The pipeline consists of the following stages:

1. Extract (E): The SimpleHttpOperator is used to make HTTP GET requests to NASA's APOD API. The response is in JSON format, containing fields like the title of the picture, the explanation, and the URL to the image.
2. Transform (T): The extracted JSON data is processed in the transform task using Airflow's TaskFlow API (with the @task decorator). This stage involves extracting relevant fields like titale, explanation, url, and date and ensuring they are in the correct format for the database.
3. Load (L): The transformed data is loaded into a Postgres table using PostgresHook. If the target table doesn't exist in the Postgres database, it is automatically as part of the DAG using a create table task.

### 🔍 My Customizations / What I Learned

- Deployed entire stack on AWS using Astro and RDS.
- Connected to Postgres via DBeaver externally.
- Refactored the DAG structure to follow modular patterns.
- Debugged and resolved Airflow provider errors (e.g. missing HTTP provider, DAG import issues).
- Learned how to manage infrastructure without keeping it always-on to avoid costs.
