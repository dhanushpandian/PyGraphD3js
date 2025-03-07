
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
import traceback
from langchain_community.llms import Ollama
from flask import Flask, render_template, jsonify, request
from neo4j import GraphDatabase
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os
from ai import ai
load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/chat": {"origins": "*"}})


URI = os.getenv('URI')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')


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

@app.route('/hfchat')
def hfchat():
    return render_template('hfchat.html')

@app.route('/reqgraph')
def reqgraph():
    return render_template('reqgraph.html')

@app.route('/schema')
def meta():
    return render_template('meta.html')


@app.route('/schema', methods=['POST'])
def meta_post():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    nodes = []
    relationships = []
    with driver.session() as session:
        # Get all schema visualization data using db.schema.visualization
        result = session.run("CALL db.schema.visualization()")

        for record in result:
            # Add nodes to the nodes list
            for node in record["nodes"]:
                node_data = {
                    "id": node["elementId"],
                    "labels": node["labels"],
                    "properties": node["properties"]
                }
                nodes.append(node_data)

            # Add relationships to the relationships list
            for relationship in record["relationships"]:
                relationship_data = {
                    "id": relationship["elementId"],
                    "type": relationship["type"],
                    "source": relationship["startNodeElementId"],
                    "target": relationship["endNodeElementId"],
                    "properties": relationship["properties"]
                }
                relationships.append(relationship_data)
    return jsonify({"nodes": nodes, "relationships": relationships})
# global flag
# flag = False
def get_ollama_response(message):
    #global flag
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
        context = "This is a helpful AI assistant ready to answer questions about the graph  data:."
        # if flag==False:
        #     context+= str(get_graph_data())
        #     flag=True
        context+= str(get_graph_data())
        
        # Invoke the chain with message and context
        response = chain.invoke({
            "context": context, 
            "input": message
        })
        
        return response
    
    except Exception as e:
        print(f"Error in Ollama response: {str(e)}")
        return f"Sorry, there was an error processing your message: {str(e)}"
    

# @app.route('/hfchat', methods=['POST'])
# def hfchat_post():
#     try:
#         # Get user input from the request
#         data = request.get_json()
#         user_message = data.get('message', '')
#         user_message = "give me consice answers only from the graph data answering the question " + user_message
#         if not user_message:
#             return jsonify({'response': 'No message provided'}), 400
#         print(f"Received message for Groq: {user_message}")
#         GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
#         GROQ_API_KEY = os.getenv("GROQ_API_KEY")
#         headers = {
#             "Content-Type": "application/json",
#             "Authorization": f"Bearer {GROQ_API_KEY}"
#         }
#         user_message += "this is a graph data, interpret it and answer the questions"
#         user_message += str(get_graph_data())
#         payload = {
#             "model": "llama3-8b-8192",
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": user_message
#                 }
#             ]
#         }
#         response = requests.post(GROQ_API_URL, headers=headers, json=payload)
#         # Check if the request was successful
#         if response.status_code == 200:
#             # Parse the response from the Groq API
#             ai_response = response.json()
#             chat_response = ai_response.get("choices", [{}])[0].get("message", {}).get("content", "No response from Groq API")
#             # Return the response to the frontend
#             return jsonify({'response': chat_response})
#         else:
#             # Log and return error if the API request failed
#             error_message = response.json().get("error", {}).get("message", "Unknown error")
#             print(f"Groq API Error: {error_message}")
#             return jsonify({'response': f"Groq API Error: {error_message}"}), response.status_code
#     except Exception as e:
#         print(f"Error in hfchat_post: {traceback.format_exc()}")
#         return jsonify({'response': f"Server Error: {str(e)}"}), 500

# import markdown2

# def convert_markdown_to_html(md_text):
#     return markdown2.markdown(md_text)



    
@app.route('/hfchat', methods=['POST'])
def hfchat_post():
    try:
        # Ensure request has the correct content type
        if not request.is_json:
            return jsonify({'response': 'Unsupported Media Type. Use application/json'}), 415

        # Get user input from the request
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'response': 'No message provided'}), 400

        user_message = "give me concise answers only from the graph data answering the question " + data['message']
        print(f"Received message for AI: {user_message}")

        # Simulate get_graph_data() function (Ensure you define this in actual implementation)
        user_message += " this is a graph data, interpret it and answer the questions"
        user_message += str(get_graph_data())  # Ensure get_graph_data() is defined

        response = ai(user_message)  # Call AI function
        # response_text = ai(user_message)  # Get AI response
        # html_response = convert_markdown_to_html(response_text)
        return jsonify(response)  # Ensure JSON response

    except Exception as e:
        print(f"Error in hfchat_post: {traceback.format_exc()}")
        return jsonify({'response': f"Server Error: {str(e)}"}), 500



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
    app.run(host='0.0.0.0', port=8080, debug=True)