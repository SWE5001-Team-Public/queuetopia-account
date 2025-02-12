# Queuetopia Account Manager

This project can be run **using Docker** or **directly as a FastAPI application**.

---

## **🔹 Prerequisites**

Make sure you have the following installed:

### **For Docker Setup**

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Bash (for running shell scripts)

### **For Running FastAPI Locally (Without Docker)**

- Python 3.10+ installed ([Download Here](https://www.python.org/downloads/))
- Pip (Python package manager)
- Virtual environment (`venv`)

---

## **🔹 Running the Application with Docker**

To build and start the Docker container, run:

```sh
./scripts/up.sh
```

### **🔹 Running in Development Mode (`--dev` Flag)**

If you want to run the app using the **development Docker Compose file**, use:

```sh
./scripts/up.sh --dev
```

### **🔹 What `up.sh` Does**

1. Moves to the **project root directory** where the `Dockerfile` is located.
2. Calls `down.sh` to stop any existing containers.
3. Builds a Docker image named `account-manager`.
4. Starts the container using `docker-compose.yml` (or `docker-compose-dev.yml` when `--dev` is passed).
5. Runs the container **in detached mode (`-d`)**.
6. Lists all running containers.

Once the script completes, the application will be running on:

```
http://localhost:5000
```

---

## **🔹 Running the FastAPI Application Locally for Development**

To run the FastAPI application locally **without Docker**, follow these steps:

### **1️⃣ Download the `.env.local` File**

Download the `.env.local` file
from [Google Drive](https://drive.google.com/drive/folders/138NUTJS-QoB0TqtaK2kPsz5nduhE3Uei?usp=sharing) and place it
in the project root.

### **2️⃣ Create & Activate a Virtual Environment**

Run these commands in the project root:

```sh
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### **3️⃣ Install Dependencies**

With the virtual environment activated, install dependencies:

```sh
pip install -r requirements.txt
```

### **4️⃣ Run the FastAPI Application**

Start the app by running:

```sh
uvicorn app:app --host 0.0.0.0 --port 5000 --reload
```

The FastAPI app should now be running at:

```
http://127.0.0.1:5000
```

---

## **🔹 Deploying the Docker Container to AWS EC2**

To deploy the application on an **AWS EC2 instance**, follow these steps:

### **1️⃣ Connect to Your EC2 Instance**

SSH into your EC2 instance:

```sh
ssh -i your-key.pem ec2-user@your-ec2-ip
```

### **2️⃣ Install Docker & Docker Compose**

If not installed, run:

```sh
sudo yum update -y
sudo yum install docker -y
sudo systemctl start docker
sudo usermod -aG docker ec2-user
```

Then install Docker Compose:

```sh
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### **3️⃣ Clone the Repository**

```sh
git clone https://github.com/SWE5001-Team-Public/queuetopia-account/queuetopia-account.git # HTTPS
git clone git@github.com:SWE5001-Team-Public/queuetopia-account.git # SSH
cd queuetopia-account
```

### **4️⃣ Download the `.env.production` File**

Download the `.env.production` file
from [Google Drive](https://drive.google.com/drive/folders/138NUTJS-QoB0TqtaK2kPsz5nduhE3Uei?usp=sharing) and place it
in the project root.

### **5️⃣ Start the Docker Container**

```sh
./scripts/up.sh --dev
```

### **6️⃣ Check the Running Container**

```sh
docker ps
```

The app should now be running on `http://your-ec2-ip:5000`

---

## **🔹 Starting & Stopping the Database**

### **Starting PostgreSQL (`db-up.sh`)**

Run:

```sh
./scripts/db-up.sh
```

This script:

1. Starts the PostgreSQL container defined in `docker-compose.yml`.
2. Waits until PostgreSQL is ready before exiting.

### **Stopping PostgreSQL (`db-down.sh`)**

Run:

```sh
./scripts/db-down.sh
```

This script:

1. Stops and removes the PostgreSQL container (`account-mgr-db`).
2. Removes the associated Docker image.
3. Cleans up unused Docker resources.

---

## **🔹 Stopping & Removing the Docker Container**

To stop and clean up the container and its image, run:

```sh
./scripts/down.sh
```

---

## **🔹 Useful Docker Commands**

| Command                       | Description                        |
|-------------------------------|------------------------------------|
| `docker ps`                   | Show running containers            |
| `docker images`               | List all images                    |
| `docker logs account-manager` | View logs of the running container |
| `docker-compose up -d`        | Start containers in detached mode  |
| `docker-compose down`         | Stop and remove containers         |

---

## **🎯 Summary**

| Command                                               | Purpose                              |
|-------------------------------------------------------|--------------------------------------|
| `./scripts/up.sh`                                     | Build and start the container        |
| `./scripts/up.sh --dev`                               | Start in development mode            |
| `./scripts/down.sh`                                   | Stop and remove the container        |
| `./scripts/db-up.sh`                                  | Start PostgreSQL container           |
| `./scripts/db-down.sh`                                | Stop and remove PostgreSQL           |
| `uvicorn app:app --host 0.0.0.0 --port 5000 --reload` | Start the FastAPI app without Docker |
| `docker ps`                                           | Check running containers             |
| `docker logs account-manager`                         | View container logs                  |

Now you can **run the application using Docker, locally for development, or deploy it to AWS EC2**! 🚀

