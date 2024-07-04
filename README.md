# Webinar Links Filtering Application

This application helps you filter and manage webinar links. It uses SerpAPI for enhanced search functionality to find relevant webinars based on your criteria.

## Description

The Webinar Links Filtering Application is designed to help users find and filter webinar links based on specific criteria. The application uses Flask for the backend and integrates with SerpAPI to enhance the search capabilities. Users can search for webinars, filter results, and save their preferred links.

## Features

- Search webinars using keywords
- Filter webinars based on specific criteria
- Save and manage webinar links
- User authentication and management
- Integration with SerpAPI for advanced search functionality

## Installation

### Prerequisites

- Python 3.x
- Git
- Flask
- Virtual environment (optional but recommended)

### Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/webinar-links-filtering.git
    cd webinar-links-filtering
    ```

2. **Create and activate a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    source venv/bin/activate  # On macOS/Linux
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the environment variables:**

    Create a `.env` file in the root directory of the project and add the following environment variables:

    ```env
    SECRET_KEY=your_secret_key_here
    SQLALCHEMY_DATABASE_URI=sqlite:///webinars.db
    SERPAPI_KEY=your_serpapi_key_here
    ```

    Replace `your_secret_key_here` with a randomly generated secret key and `your_serpapi_key_here` with your SerpAPI key.

5. **Initialize the database:**

    Open a Python shell and run the following commands to create the database tables:

    ```bash
    python
    ```

    ```python
    from application import app, db
    with app.app_context():
        db.create_all()
    exit()
    ```

6. **Run the application:**

    ```bash
    flask run
    ```

    The application will be available at `http://127.0.0.1:5000/`.

## SerpAPI Integration

This application uses SerpAPI to enhance the search functionality. Follow these steps to integrate SerpAPI:

1. **Sign up for SerpAPI:**

    Go to [SerpAPI](https://serpapi.com/) and sign up for an account.

2. **Get your SerpAPI key:**

    After signing up, go to your SerpAPI dashboard and get your API key.

3. **Set the SERPAPI_KEY environment variable:**

    Add your SerpAPI key to the `.env` file as shown above.

4. **Update the search functionality in your Flask application:**

    Ensure that your search routes and functions use the SerpAPI key to make requests and process the search results.

    Example search function:

    ```python
    import requests
    import os

    SERPAPI_KEY = os.getenv('SERPAPI_KEY')

    def search_webinars(query):
        params = {
            'engine': 'google',
            'q': query,
            'api_key': SERPAPI_KEY,
        }
        response = requests.get('https://serpapi.com/search', params=params)
        return response.json()
    ```

Screenshots:

(image1.png)

(image2.png)

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes or improvements.
