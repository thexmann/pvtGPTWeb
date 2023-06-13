#!/usr/bin/env python3

# The web interface was added by Cedar Creek Technologies, LLC
# Other changes to accomidate the web by CCT
# Modifications made June 2023
# Cedar Creek Technologies, LLC, New Mexico, USA
# cedardteektech_at_cchristmann.com
# Web Interface:
#     GET:  /                             Return webpage in static folder
#     POST: /query {query:question_text}  Ask a question and get the return
#     POST: /terminate {}                 End the program


from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All, LlamaCpp
from flask import Flask, request, jsonify, send_from_directory
import os
import sys
import argparse

# Get the directory path of the current script file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set the current working directory to the script directory
os.chdir(script_dir)
print("Running from ",script_dir)

load_dotenv()

embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")
persist_directory = os.environ.get('PERSIST_DIRECTORY')

model_type = os.environ.get('MODEL_TYPE')
model_path = os.environ.get('MODEL_PATH')
model_n_ctx = os.environ.get('MODEL_N_CTX')
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',4))

from constants import CHROMA_SETTINGS

app = Flask(__name__, static_folder='static')

# Set up the query answering chain
embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings, client_settings=CHROMA_SETTINGS)
retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})

callbacks = [StreamingStdOutCallbackHandler()]  # always activate the streaming StdOut callback for LLMs

# Prepare the LLM
match model_type:
    case "LlamaCpp":
        llm = LlamaCpp(model_path=model_path, n_ctx=model_n_ctx, callbacks=callbacks, verbose=False)
    case "GPT4All":
        llm = GPT4All(model=model_path, n_ctx=model_n_ctx, backend='gptj', callbacks=callbacks, verbose=False)
    case _default:
        print(f"Model {model_type} not supported!")
        exit()

qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

@app.route("/")
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/terminate", methods=["POST"])
def terminate():
    print("Terminating the application...")
    sys.exit(0)

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    print("Query:", query)  # Print the query to the console

    # Get the answer from the chain
    res = qa(query)
    answer, docs = res['result'], res['source_documents']

    # Format the result
    result = {
        "question": query,
        "answer": answer,
        "source_documents": [{'source': document.metadata["source"], 'content': document.page_content} for document in docs]
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=False)
