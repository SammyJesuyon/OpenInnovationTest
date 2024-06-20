```markdown
# Flask Image API

This is a Flask-based web application that processes image data from a CSV file, stores it in a SQLite database, and provides an API to request image frames based on depth values.

## Table of Contents

- [Setup](#setup)
- [Running Locally](#running-locally)
- [Docker Deployment](#docker-deployment)
- [API Endpoints](#api-endpoints)
- [License](#license)


## Setup

### Prerequisites

- Python 3.9 or higher
- Docker (for Docker deployment)
- GitHub account (for cloud deployment)

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/SammyJesuyon/OpenInnovationTest.git
   cd your repository
   ```

2. Create a virtual environment and activate it:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## Running Locally

1. Ensure you have the CSV file (`img.csv`) in the project directory.

2. Run the Flask application:

   ```sh
   python app.py
   ```

3. Open your web browser and navigate to `http://localhost:3000`.

## Docker Deployment

1. Build the Docker image:

   ```sh
   docker build -t image-api .
   ```

2. Run the Docker container:

   ```sh
   docker run -p 3000:3000 image-api
   ```

3. Open your web browser and navigate to `http://localhost:3000`.


## API Endpoints

### `/image_frames`

- **Method:** GET
- **Description:** Retrieve image frames based on depth values.
- **Query Parameters:**
  - `depth_min` (integer): Minimum depth value.
  - `depth_max` (integer): Maximum depth value.
- **Response:** Returns a PNG image of the combined frames.

#### Example

```sh
curl "http://localhost:3000/image_frames?depth_min=9000&depth_max=9010"
```
