
# Note On Docker

Docker is a containerization software that allows us to isolate software in a similar way to virtual machines but in a much leaner way.

A Docker image is a snapshot of a container that we can define to run our software, or in this case our data pipelines. By exporting our Docker images to Cloud providers such as Amazon Web Services or Google Cloud Platform we can run our containers there.

## Basic Docker Command
Check Docker version
```bash
docker --version
```

Run simple docker container 
```bash
docker run hello-world
```

Run something more complex:

```bash
docker run ubuntu
```
Nothing happens. Need to run it in -it mode:

```bash
docker run -it ubuntu
```

### Managing Containers
We can see all running containers with:
```bash

docker ps -a
```

### Different Base Images
There are other base images besides hello-world and ubuntu. For example, Python:

```bash
docker run -it --rm python:3.9.
# add -slim to get a smaller version
```

This one starts python. If we want bash, we need to overwrite entrypoint:

```bash
docker run -it \
    --rm \
    --entrypoint=bash \
    python:3.9.16-slim
```    

# Docker Volume
Docker volumes are a way to persist data between docker containers.
We can mount a folder on our local machine to a docker container.

```bash
docker run -it \
    --rm \
    --entrypoint=bash \
    -v $(pwd)/your_folder/file_to_mount:/your_folder/file_to_mount \
    python:3.9.16-slim
```

Inside the container, run:

```bash
cd folder_to_mount
ls -la

# All the files are in the folder
```
## Dockerizing our project

### Simple Dockerfile With pip
```bash

# base Docker image that we will build on
FROM python:3.13.11-slim

# set up our image by installing prerequisites; pandas in this case
RUN pip install pandas pyarrow

# set up the working directory inside the container
WORKDIR /app
# copy the script to the container. 1st name is source file, 2nd is destination
COPY pipeline.py pipeline.py

# define what to do first when the container runs
# in this example, we will just run the script
ENTRYPOINT ["python", "pipeline.py"]
```

### Explanation:

FROM: Base image (Python 3.13)
- RUN: Execute commands during build
- WORKDIR: Set working directory
- COPY: Copy files into the image
- ENTRYPOINT: Default command to run


### Build and Run
Let's build the image:

```bash
docker build -t test:pandas .
```
The image name will be ``test` and its tag will be `pandas`. If the tag isn't specified it will default to `latest`.
We can now run the container and pass an argument to it, so that our pipeline will receive it:

```bash
docker run -it test:pandas some_number
```

## Dockerfile with uv
Lets use uv instead of pip

```bash
# Start with slim Python 3.13 image
FROM python:3.13.10-slim

# Copy uv binary from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set working directory
WORKDIR /app

# Add virtual environment to PATH so we can use installed packages
ENV PATH="/app/.venv/bin:$PATH"

# Copy dependency files first (better layer caching)
COPY "pyproject.toml" "uv.lock" ".python-version" ./
# Install dependencies from lock file (ensures reproducible builds)
RUN uv sync --locked

# Copy application code
COPY pipeline.py pipeline.py

# Set entry point
ENTRYPOINT ["python", "pipeline.py"]
```
Build and Run the docker image .


## Running Postgres With Docker
### Running Postgres Container
```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```

### Explanation Of Parameters:
-   -e sets environment variables (user, password, database name)
-   -v ny_taxi_postgres_data:/var/lib/postgresql creates a named volume
-   Docker manages this volume automatically
-   Data persists even after container is removed
-   Volume is stored in Docker's internal storage
-   -p 5432:5432 maps port 5432 from container to host
-   postgres:18 uses PostgreSQL version 18 (latest as of Dec 2025)

## Connecting To PostgresSql

Once the container is running, we can log into our database with pgcli.

Install pgcli:

```bash
uv add --dev pgcli
```
The --dev flag marks this as a development dependency (not needed in production). It will be added to the [dependency-groups] section of pyproject.toml instead of the main dependencies section.

Now use it to connect to Postgres:

```bash
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

uv run executes a command in the context of the virtual environment
- -h is the host. Since we're running locally we can use localhost.
- -p is the port.
- -u is the username.
- -d is the database name.
The password is not provided; it will be requested after running the command.
When prompted, enter the password: root


## Running PgAdmin With Docker
```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  dpage/pgadmin4
```
The -v pgadmin_data:/var/lib/pgadmin volume mapping saves pgAdmin settings (server connections, preferences) so you don't have to reconfigure it every time you restart the container.

### Parameters Explained
- The container needs 2 environment variables: a login email and a password. We use admin@admin.com and root in this example.
- pgAdmin is a web app and its default port is 80; we map it to 8085 in our localhost to avoid any possible conflicts.
- The actual image name is dpage/pgadmin4.
Note: This won't work yet because pgAdmin can't see the PostgreSQL container. They need to be on the same Docker network!

# Docker Network
lets create a docker network called pg-network.

```bash
docker network create pg-network
```

### Run Containers on the Same Network
Stop both containers and re-run them with the network configuration:
```bash
# Run PostgreSQL on the network
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  --network=pg-network \
  --name pgdatabase \
  postgres:18

# In another terminal, run pgAdmin on the same network
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```
- Just like with the Postgres container, we specify a network and a name for pgAdmin.
- The container names `(pgdatabase and pgadmin)` allow the containers to find each other within the network.


### Connect pgAdmin to PostgreSQL
You should now be able to load pgAdmin on a web browser by browsing to `http://localhost:8085`. Use the same email and password you used for running the container to log in.

1. Open browser and go to `http://localhost:8085`
2. Login with email: admin@admin.com, password: root
3. Right-click "Servers" → Register → Server
4. Configure:
    - General tab: Name: Local Docker
    - Connection tab:
        * Host: pgdatabase (the container name)
        * Port: 5432
        * Username: root
        * Password: root
        * Save

Now you can explore the database using the pgAdmin interface





### Dockerizing the Ingestion Script

Now let's containerize the ingestion script so we can run it in Docker.

The Dockerfile
The pipeline/Dockerfile shows how to containerize the ingestion script:

```bash
    FROM python:3.13.11-slim
    COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

    WORKDIR /code
    ENV PATH="/code/.venv/bin:$PATH"

    COPY pyproject.toml .python-version uv.lock ./
    RUN uv sync --locked

    COPY ingest_data.py .

    ENTRYPOINT ["python", "ingest_data.py"]
```
### Explanation
-  python:3.13.11-slim: Start with slim Python 3.13 image for smaller size
- COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/: Copy uv binary from official uv image
- WORKDIR /code: Set working directory inside container
- ENV PATH="/code/.venv/bin:$PATH": Add virtual environment to PATH
- COPY pyproject.toml .python-version uv.lock ./: Copy dependency files first (better caching)
- RUN uv sync --locked: Install all dependencies from lock file (ensures reproducible builds)
- COPY ingest_data.py .: Copy ingestion script
- ENTRYPOINT ["python", "ingest_data.py"]: Set entry point to run the ingestion script

Build the Docker Image
```bash
cd pipeline
docker build -t taxi_ingest:v001 .
```

### Run the Containerized Ingestion
```bash
docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table=yellow_taxi_trips
```
Important Notes
We need to provide the network for Docker to find the Postgres container. It goes before the name of the image.
Since Postgres is running on a separate container, the host argument will have to point to the container name of Postgres (pgdatabase).
You can drop the table in pgAdmin beforehand if you want, but the script will automatically replace the pre-existing table.

## Docker Compose
docker-compose allows us to launch multiple containers using a single configuration file, so that we don't have to run multiple complex docker run commands separately.

Docker compose makes use of YAML files. Here's the docker-compose.yaml file:

```bash
services:
  pgdatabase:
    image: postgres:18
    environment:
      POSTGRES_USER: "root"
      POSTGRES_PASSWORD: "root"
      POSTGRES_DB: "ny_taxi"
    volumes:
      - "ny_taxi_postgres_data:/var/lib/postgresql"
    ports:
      - "5432:5432"

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: "admin@admin.com"
      PGADMIN_DEFAULT_PASSWORD: "root"
    volumes:
      - "pgadmin_data:/var/lib/pgadmin"
    ports:
      - "8085:80"



volumes:
  ny_taxi_postgres_data:
  pgadmin_data:
```
### Explanation
- We don't have to specify a network because `docker-compose` takes care of it: every single container (or "service", as the file states) will run within the same network and will be able to find each other according to their names (`pgdatabase` and `pgadmin` in this example).
- All other details from the docker run commands (environment variables, volumes and ports) are mentioned accordingly in the file following YAML syntax.
Start Services with Docker Compose

### Start Services with Docker Compose
We can now run Docker compose by running the following command from the same directory where `docker-compose.yaml` is found. Make sure that all previous containers aren't running anymore:

```bash
docker-compose up
```

Detached Mode
If you want to run the containers again in the background rather than in the foreground (thus freeing up your terminal), you can run them in detached mode:
```bash
docker-compose up -d
```

Stop Services
You will have to press Ctrl+C in order to shut down the containers when running in foreground mode. The proper way of shutting them down is with this command:
```bash
docker-compose down
```