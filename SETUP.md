# Project Setup Instructions

## Prerequisites
Before setting up the project, make sure you have the following installed on your local machine:

- **Python** (for FastAPI backend)
- **Node.js** and **npm** (for React.js frontend)
- **credentials** (put your 'credentials' file in google_credentials folder.)
- **REACT_APP_MAPBOX_ACCESS_TOKEN** (create .env frontend file and add your MapBox Token.)

## 1. Clone the Repository
First, clone the repository to your local machine:
```sh
git clone https://github.com/Muhammad-Bilal-Akram/AirQualityFullStack.git
```

## 2. Backend Setup (FastAPI)
Navigate to the Backend Directory
```sh
cd backend
```

### Create a Virtual Environment  
- **For Linux/macOS:**
```sh
  python3 -m venv venv
  source venv/bin/activate
```

- **For Windows**
```sh
  python -m venv venv
  venv\Scripts\activate
```

### Install Backend Dependencies
```sh
pip install -r backend/requirements.txt
```

### Run the Backend Server via Terminal
```sh
python main.py
```

This will start the FastAPI server on http://127.0.0.1:8000. You can now access your API endpoints.

## 3. Frontend Setup (React.js)
Navigate to the Frontend Directory
```sh
cd frontend
```

### Install Frontend Dependencies
Install the necessary dependencies using npm:
```sh
npm install
```

### Run the Frontend Development Server via Terminal
```sh
npm start
```

This will launch the React app on http://localhost:3000 and open it in your browser.

## 4. Docker Setup (Optional)
If you prefer to run the project using **Docker Compose**, follow these steps:

### **Prerequisites**
Make sure you have **Docker** and **Docker Compose** installed:
- [Download Docker](https://www.docker.com/get-started)
- Check installation:
  ```sh
  docker --version
  docker-compose --version
    ```

#### **Steps to Run Using Docker Compose**
1. Navigate to the project root directory:
```sh
cd AirQualityFullStack
```

2. Build and start the containers:
```sh
docker-compose up --build
```

3. The backend (FastAPI) and frontend (React.js) will start inside Docker containers:
 - Backend (FastAPI): http://127.0.0.1:8000
 - Frontend (React.js): http://localhost:3000

4. To stop the containers:
```sh
docker-compose down
```

