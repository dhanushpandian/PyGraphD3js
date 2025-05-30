# PyGraphD3js
# Neo4j Graph Visualization API

This project provides an interactive web-based visualization of a Neo4j graph using Flask, D3.js, and environment variables for secure configuration management.

The application retrieves schema data from a Neo4j database using the `CALL db.schema.visualization()` query and displays nodes and relationships in a dynamic and interactive graph. The front-end is built with D3.js for rendering the graph and handling user interactions like zooming and panning.

## Features

- **Interactive Graph Visualization**: The graph is visualized with nodes and relationships, which can be zoomed, panned, and hovered to display detailed information.
- **Dynamic Schema**: Fetches the schema visualization from the Neo4j database and renders it dynamically.
- **Environment Configuration**: Uses a `.env` file to manage sensitive configuration like database credentials securely.

## Technologies Used

- **Backend**: Flask (Python)
- **Database**: Neo4j
- **Frontend**: D3.js (for graph visualization)
- **Environment Management**: Python-dotenv (for managing environment variables)

## Setup and Installation

Before you start, ensure you have the following installed:

- [Python 3.7+](https://www.python.org/downloads/)
- [Neo4j Database](https://neo4j.com/download/)
- [pip](https://pip.pypa.io/en/stable/)


Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/neo4j-graph-visualization.git
cd neo4j-graph-visualization
