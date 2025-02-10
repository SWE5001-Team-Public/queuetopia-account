# Queuetopia Account Manager

This project can be run **using Docker** or **directly as a Flask application**.

---

## **🔹 Prerequisites**

Make sure you have the following installed:

### **For Docker Setup**

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Bash (for running shell scripts)

### **For Running Flask Locally (Without Docker)**

- Python 3.10+ installed ([Download Here](https://www.python.org/downloads/))
- Pip (Python package manager)
- Virtual environment (`venv`)

---

## **🔹 Running the Application with Docker**

To build and start the Docker container, run:

```sh
./scripts/up.sh
```

### **🔹 What `up.sh` Does**

1. Moves to the **project root directory** where the `Dockerfile` is located.
2. Builds a Docker image named `account-manager`.
3. Starts the container using `docker-compose.yml` from the `scripts/` directory.
4. Runs the container **in detached mode (`-d`)** with the name `account-manager`.
5. Lists all running containers.

Once the script completes, the application will be running on:

```
http://localhost:5000
```

---

## **🔹 Stopping & Removing the Docker Container**

To stop and clean up the container and its image, run:

```sh
./scripts/down.sh
```

### **🔹 What `down.sh` Does**

1. Stops and removes the `account-manager` container.
2. Removes the Docker image named `queuetopia-account-manager`.
3. Cleans up unused Docker resources using:
   ```sh
   docker system prune -af
   ```
4. Lists all remaining containers.

---

## **🔹 Running the Flask App Without Docker**

If you want to run the app **directly as a Flask application**, follow these steps:

### **1️⃣ Create & Activate a Virtual Environment**

Run these commands in the project root:

```sh
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### **2️⃣ Install Dependencies**

With the virtual environment activated, install dependencies:

```sh
pip install -r requirements.txt
```

### **3️⃣ Run the Flask Application**

Start the app by running:

```sh
python app.py
```

The Flask app should now be running at:

```
http://127.0.0.1:5000
```

---

## **🔹 How the Docker Setup Works**

### **1️⃣ `Dockerfile` (Container Configuration)**

The `Dockerfile` defines how the Python application is containerized:

- Uses **Python 3.10-slim** as the base image.
- Sets up `/app` as the working directory.
- Installs dependencies from `requirements.txt`.
- Copies application files into the container.
- Exposes port **5000**.
- Runs `app.py` when the container starts.

### **2️⃣ `docker-compose.yml` (Container Orchestration)**

Located inside `./scripts/`, the `docker-compose.yml` defines the container:

- **Container Name:** `account-manager`
- **Build Context:** `../` (project root where `Dockerfile` is located)
- **Port Mapping:** Exposes port `5000` on the host
- **Restart Policy:** `always` (ensures the container restarts on failure)
- **Startup Command:** Runs `python app.py` inside the container

---

## **🔹 Useful Docker Commands**

| Command                       | Description                        |
| ----------------------------- | ---------------------------------- |
| `docker ps`                   | Show running containers            |
| `docker images`               | List all images                    |
| `docker logs account-manager` | View logs of the running container |
| `docker-compose up -d`        | Start containers in detached mode  |
| `docker-compose down`         | Stop and remove containers         |

---

## **🔹 Troubleshooting**

### **Container Not Starting?**

- Run:
  ```sh
  docker logs account-manager
  ```
- Check for missing dependencies or port conflicts.

### **Port 5000 Already in Use?**

- Find the process using port 5000:
  ```sh
  sudo lsof -i :5000
  ```
- Kill the process:
  ```sh
  sudo kill -9 <PID>
  ```

### **Docker Daemon Not Running?**

- Start Docker:
  ```sh
  sudo systemctl start docker
  ```

---

## **🎯 Summary**

| Command                       | Purpose                            |
| ----------------------------- | ---------------------------------- |
| `./scripts/up.sh`             | Build and start the container      |
| `./scripts/down.sh`           | Stop and remove the container      |
| `python app.py`               | Start the Flask app without Docker |
| `docker ps`                   | Check running containers           |
| `docker logs account-manager` | View container logs                |

Now you can **run the application using Docker or directly as a Flask app**! 🚀
