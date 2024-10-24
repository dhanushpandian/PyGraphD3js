from flask import Flask, render_template, jsonify
from neo4j import GraphDatabase
import json

app = Flask(__name__)

# Neo4j connection configuration
URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "12345678"

def get_graph_data():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    nodes = []
    relationships = []
    
    with driver.session() as session:
        # Get all nodes
        node_result = session.run("""
            MATCH (n)
            RETURN id(n) as id, labels(n) as labels, properties(n) as properties
        """)
        
        for record in node_result:
            node = {
                "id": record["id"],
                "labels": record["labels"],
                "properties": record["properties"]
            }
            nodes.append(node)
            
        # Get all relationships
        rel_result = session.run("""
            MATCH (a)-[r]->(b)
            RETURN id(r) as id, type(r) as type, 
                   id(a) as source, id(b) as target,
                   properties(r) as properties
        """)
        
        for record in rel_result:
            relationship = {
                "id": record["id"],
                "type": record["type"],
                "source": record["source"],
                "target": record["target"],
                "properties": record["properties"]
            }
            relationships.append(relationship)
    
    return {"nodes": nodes, "relationships": relationships}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/graph')
def get_graph():
    try:
        graph_data = get_graph_data()
        return jsonify(graph_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001,debug=True)