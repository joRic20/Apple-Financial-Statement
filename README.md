# Apple Financial Statement Viewer

> A Streamlit-based web application that retrieves and visualizes Apple Inc.'s annual income statement data (Total Revenue) using the Alpha Vantage API. Deployed seamlessly on CapRover for easy access and scalability.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
6. [Usage](#usage)
7. [Configuration](#configuration)
8. [Deployment on CapRover](#deployment-on-caprover)
9. [Project Structure](#project-structure)
10. [Contributing](#contributing)
11. [License](#license)
12. [Contact](#contact)

---

## Project Overview

The **Apple Financial Statement Viewer** is a simple yet powerful web application built with **Streamlit**. It fetches Apple Inc.'s annual income statement data via the **Alpha Vantage API**, processes that data into a pandas DataFrame, and renders a bar chart of Apple's total revenue over the years.

Key objectives:

* Demonstrate secure API integration using environment variables.
* Perform data processing and type conversion with pandas.
* Visualize financial metrics using Matplotlib within a Streamlit app.
* Show a complete CI/CD workflow by deploying to **CapRover**.

This repository contains all source code, configuration files, and documentation needed to run and deploy this application locally or on a cloud server.

---

## Features

* **Income Statement Retrieval**: Automatically pulls annual income statements for Apple (AAPL) from Alpha Vantage.
* **Data Processing**: Converts string values to numeric types, extracts fiscal years, and sorts data chronologically.
* **Interactive Visualization**: Displays a bar chart of total revenue (in billions USD) for each fiscal year.
* **Environment Configuration**: Reads API keys from a `.env` file for security.
* **Containerized Deployment**: Provides a Dockerfile for containerization.
* **Scalable Hosting**: Includes instructions for deploying on CapRover.

---

## Tech Stack

* **Python 3.11**
* **Streamlit** for web application framework
* **pandas** for data manipulation
* **requests** for API calls
* **Matplotlib** for plotting
* **python-dotenv** for loading environment variables
* **Docker** for containerization
* **CapRover** for PaaS deployment

---

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

* Python 3.8 or higher
* pip (Python package manager)
* Docker (for local container builds)
* Git (for version control)
* Node.js and npm (required for CapRover CLI, if deploying)

You will also need:

* An **Alpha Vantage API key** (free to obtain at [https://www.alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key)).
* A **CapRover** server (self-hosted or managed) with access credentials.

---

## Installation

Follow these steps to clone the repository and install dependencies locally:

```bash
# 1. Clone the repository
git clone https://github.com/joric20/Apple-Financial-Statement.git
cd Apple-Financial-Statement

# 2. Create (or activate) a Python virtual environment
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate  # Windows

# 3. Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Create a .env file in the project root with your Alpha Vantage API key
#    (See [Configuration](#configuration) for details)
```

---

## Usage

Once installed, you can run the Streamlit app locally to verify functionality:

```bash
# 1. Activate your virtual environment (if not already active)
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate  # Windows

# 2. Run the Streamlit app
streamlit run app.py
```

* Open your browser and navigate to `http://localhost:8501`.
* The app will display Apple’s annual total revenue in a bar chart.

---

## Configuration

The application requires an **Alpha Vantage API key** to fetch financial data. We use a `.env` file (loaded by **python-dotenv**) for security.

1. In the project’s root directory, create a file named `.env`.
2. Add the following line (replace `YOUR_API_KEY` with your actual key):

   ```env
   AV_TOKEN=YOUR_API_KEY
   ```
3. Save and close the file.

The Streamlit app reads this environment variable using:

```python
from dotenv import load_dotenv
import os

load_dotenv()
av_token = os.getenv("AV_TOKEN")
```

Ensure you do **not** commit `.env` to Git: it’s already included in `.gitignore`.

---

## Deployment on CapRover

This section explains how to deploy the containerized app to a CapRover server.

### 1. Create `caprover.json` (optional)

You can include a `caprover.json` in your project root to simplify CLI deployments:

```json
{
  "caproverMinimumRequiredVersion": "2.0.0",
  "appName": "Apple-Financial-Statement",
  "dockerfilePath": "./Dockerfile",
  "stopPreviousContainer": true
}
```

* `appName` must exactly match the app name you created in the CapRover UI.
* `dockerfilePath` is the relative path to your Dockerfile.

### 2. Build & Test Locally (Optional)

You can verify your Docker container locally before pushing to CapRover:

```bash
# 1. Build the image
docker build -t apple-fin-stmt .

# 2. Run the container, supplying the environment variable
docker run -p 8501:8501 -e AV_TOKEN=YOUR_API_KEY apple-fin-stmt

# 3. In your browser, navigate to http://localhost:8501
```

### 3. Set Environment Variables on CapRover

1. Log in to your CapRover dashboard.
2. Navigate to your app (**Apple-Financial-Statement**) → **App Configs** → **Environment Variables**.
3. Add:

   * **Key**: `AV_TOKEN`
   * **Value**: `YOUR_API_KEY`
4. Save & Update.

### 4. Deploy via CapRover CLI

1. Install CapRover CLI (if not already):

   ```bash
   npm install -g caprover
   ```

2. Log in to your CapRover server:

   ```bash
   caprover login
   # Enter your CapRover URL (e.g., https://captain.example.com)
   # Enter your root password
   ```

3. From your project root (`Apple-Financial-Statement/`), run:

   ```bash
   caprover deploy
   ```

   * If you didn’t create `caprover.json`, use:

     ```bash
     caprover deploy --appName Apple-Financial-Statement --dockerfilePath ./Dockerfile
     ```

4. Wait for the build and deployment to complete. You’ll see “Deployment successful.”

5. Visit your live URL:

   ```
   https://appl.quandev.xyz
   ```

That’s it! Your Streamlit app should now be live and accessible.

---

## Project Structure

```
Apple-Financial-Statement/
├── .env                  # Environment variables (ignored by Git)
├── .gitignore            # Git ignore list
├── caprover.json         # CapRover deployment configuration
├── Dockerfile            # Dockerfile for building the container
├── requirements.txt      # Python dependencies
├── app.py                # Main Streamlit application
├── assets/               # (Optional) logos, images, or CSS
│   └── logo.png          # Project logo (if used)
├── README.md             # This documentation file
└── ...                   # Any other scripts or data
```

---

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/joric20/Apple-Financial-Statement/issues).

1. Fork the repository.
2. Create your feature branch:

   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes:

   ```bash
   git commit -m "Add some AmazingFeature"
   ```
4. Push to the branch:

   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request.

Please make sure to update tests as appropriate, and adhere to the existing code style.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

