# pvtGPTWeb.py
A web REST interface added to privateGPT

## Overview
This is very basic web interface, but it does allow you to query privateGPT from a web interface.
Feel free to create your own webpage to access the REST endpoints. The webpage is located in the
static directory and must be named index.html.

## Startup
See the privateGPT GitHub page to set up the privateGPT application. The pvtGPTWeb.py app can be
use in place of the privateGPT.py. If you want a CLI interface, use privateGPT.py.

Place the pvtGPTWeb.py application into your privateGPT folder.
Place the static folder with the index.html file into your privateGPT folder.

## Run the AI App
After you have ingested your data, start the pvtGPTWeb application

python pvtGPTWeb.py

Wait for the python application to initialize.

## Ask your questions
In your browser, navigate to the webpage: http://localhost:5000.
Type your question into the text box and click "Query".
The privateGPT base application takes a while to create an answer. The web interface shows a timer while
the AI creates its response.

To ask another question, type your new question in the textbox.

## REST Interface
GET:  /                             - Return webpage in static folder

POST: /query {query:question_text}  - Ask a question and get the return

POST: /terminate {}                 - End the AI program

## Original application
For more information on privateGPT, see the original GitHub page: https://github.com/imartinez/privateGPT
