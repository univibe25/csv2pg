# csv2pg

A Python utility for loading CSV files into PostgreSQL databases efficiently using Polars for fast data processing.

## Features

- Fast CSV loading using Polars
- PostgreSQL integration with SQLAlchemy
- Command-line interface with Typer
- Environment variable support with python-dotenv
- Docker support for easy deployment

## Requirements

- Python 3.13 or higher
- PostgreSQL database
- Docker (optional, for containerized deployment)

## Installation

### Using pip

```bash
pip install git+https://github.com/univibe25/csv2pg.git
```

### Using uv (recommended)

```bash
uv pip install git+https://github.com/univibe25/csv2pg.git
```

## Usage

### Basic Usage

```bash
uv run csv2pg loadcsv --url postgresql://user:password@host:port/database
```

### Environment Variables

You can use environment variables for configuration:

```bash
export DATABASE_URL="postgresql://user:password@host:port/database"
uv run csv2pg loadcsv
```

## Docker Deployment

You can use Docker Compose to set up both the PostgreSQL database and the CSV loader:

```yaml
# docker-compose.yml
version: "3"
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypw
      POSTGRES_DB: mydb
    ports: ["5432:5432"]

  loader:
    image: python:3.12-slim
    command: >
      bash -c "
        pip install uv &&
        uv pip install git+https://github.com/univibe25/csv2pg.git &&
        csv2pg loadcsv --url postgresql://myuser:mypw@db:5432/mydb
      "
    depends_on: [db]
```

To start the services:

```bash
docker-compose up
```

## Development

1. Clone the repository:
```bash
git clone https://github.com/univibe25/csv2pg.git
cd csv2pg
```

2. Create a virtual environment and install deps:
```bash
uv sync
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.