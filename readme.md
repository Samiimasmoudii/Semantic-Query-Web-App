# Semantic Web Application

## Overview
This project is a web-based application that allows users to construct and execute SPARQL queries on DBpedia. It provides a user-friendly interface for exploring linked data, with features like query suggestions powered by Elasticsearch, a custom query builder, and visualization options for query results.

## Features
- **User Authentication**: Secure signup and login with password hashing.
- **SPARQL Query Execution**: Users can run SPARQL queries on DBpedia.
- **Elasticsearch Integration**: Suggests queries as users type.
- **Query Visualization**: Displays results in tables.
- **Query History Management**: Save and export queries in CSV or JSON.
- **Security**: Protection against SPARQL injection, CSRF, and secure password handling.

## Tech Stack
- **Backend**: Flask (Python)
- **Frontend**: JavaScript, Bootstrap
- **Database**: MySQL (Dockerized)
- **Search Engine**: Elasticsearch (Dockerized)
- **SPARQL Endpoint**: DBpedia
- **Containerization**: Docker Compose

## Project Structure
```
semantic-web-app/
│
├── app/
│   ├── templates/          # HTML files
│   ├── static/             # CSS, JavaScript
│   ├── controllers/        # elastic Searc, Sparql Utils
│   ├── models/             # models
│   ├── __init__.py         # Flask app initialization
│   ├── routes.py           # Define routes and business logic
│   ├── sparql_utils.py     # SPARQL query functions
│   ├── database.py         # Database utilities 
│   └── config.py               # Configuration settings
│
├── tests/                  # Unit and integration tests
├── Docker/
    └── docker-compose.yml      
│
├── 
├── run.py                  # Main script to run the Flask app
├── requirements.txt        # Dependencies
    
```

## Setup & Installation
### Prerequisites
- Docker & Docker Compose
- Python 3.8+
- Node.js (optional for frontend enhancements)

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/semantic-web-app.git
   cd semantic-web-app
   ```
2. Build and start the services:
   ```sh
   docker-compose up -d
   ```
3. Install Python dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the Flask app:
   ```sh
   python run.py
   ```
5. Open `http://localhost:5000` in your browser.

## API Endpoints
| Method | Endpoint           | Description                  |
|--------|-------------------|------------------------------|
| GET    | `/`               | Home page                    |
| POST   | `/login`          | User authentication          |
| POST   | `/signup`         | User registration            |
| GET    | `/query`          | Run SPARQL query             |
| GET    | `/history`        | Retrieve saved queries       |

## Security Considerations
- Uses **password hashing** for secure storage.
- Implements **CSRF protection** in forms.
- Prevents **SPARQL injection** through proper query sanitization.

## Future Enhancements
- Advanced query visualizations (graphs, timelines,maps)
- OAuth-based login (Google, GitHub)
- Multi-user collaboration for queries

## License

---
**Author:** Sami MASMOUDI

