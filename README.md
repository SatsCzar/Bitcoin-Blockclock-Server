# Bitcoin Blockclock Server

This is a simple API built using Python and FastAPI to fetch and cache the current Bitcoin price from CoinLib. It uses an in-memory SQLite database to cache the data for 5 minutes.

## Requirements

- Python 3.10+
- FastAPI
- Uvicorn
- Requests

## Installation

1. Clone the repository:
```bash
git clone https://github.com/SatsCzar/Bitcoin-Blockclock-Server.git
cd Bitcoin-Blockclock-Server
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Start the API using Uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

The API has only one endpoint:
```
GET /bitcoin/{currency}
```
Replace `{currency}` with the desired currency (e.g., `BRL`, `USD`, etc.).

## Project Structure

The project contains two main files:
- `main.py`: The FastAPI application.
- `database.py`: The SQLite database configuration.

## License

This project is unlicensed.
