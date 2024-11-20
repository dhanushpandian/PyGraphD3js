
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
import traceback
from langchain_community.llms import Ollama
from flask import Flask, render_template, jsonify, request
from neo4j import GraphDatabase
from flask_cors import CORS
import requests

app = Flask(__name__)

CORS(app, resources={r"/chat": {"origins": "*"}})

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

@app.route('/api/graph')
def get_graph():
    try:
        graph_data = get_graph_data()
        return jsonify(graph_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/all')
def all():
    return render_template('alll.html')


def get_ollama_response(message):
    try:
        # Define a template with context
        template = """
        Answer the question based on the conversation history:

        Conversation History: {context}
        
        Question: {input}
        
        Answer:
        """
        
        # Initialize the model
        model = Ollama(model="llama3.1:8b")
        
        # Create a prompt template
        prompt = ChatPromptTemplate.from_template(template)
        
        # Create a chain
        chain = prompt | model
        
        # Maintain a context (you can expand this logic in your application)
        context = "This is a helpful AI assistant ready to answer questions."
        
        # Invoke the chain with message and context
        response = chain.invoke({
            "context": context, 
            "input": message
        })
        
        return response
    
    except Exception as e:
        print(f"Error in Ollama response: {str(e)}")
        return f"Sorry, there was an error processing your message: {str(e)}"
    

@app.route('/chat', methods=['POST'])
def chat_post():
    # data = request.get_json()
    # return jsonify({'response': data.get('message', '')})

   
    try:
        data = request.get_json()
        user_message = data.get('message', '')

        # Logging input
        print(f"Received message: {user_message}")

        ai_response = get_ollama_response(user_message)
       
        return jsonify({'response': ai_response})

    except Exception as e:
        print(f"Flask Route Error: {traceback.format_exc()}")
        return jsonify({'response': f'Server Error: {str(e)}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)