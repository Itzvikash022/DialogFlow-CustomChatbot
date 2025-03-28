import os
from dotenv import load_dotenv

import json
# Remove the incorrect import as it is not needed
# import dialogflow
from google.cloud import dialogflow_v2 as dialogflow
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from any origin (Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

with open("D:/Projects/ChatBot/agentx-mhro-a8846cad656d.json", "r") as file:
    data = json.load(file)


# Path to your Google Dialogflow service account JSON key
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:/Projects/ChatBot/agentx-mhro-a8846cad656d.json"

# Load environment variables from .env
load_dotenv()


# Read credentials from .env
creds_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if creds_json:
    creds_dict = json.loads(creds_json)
    with open("service-account.json", "w") as f:
        json.dump(creds_dict, f)  # Temporarily write to a file

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"

print("Project ID:", data["project_id"])
print("Service Account Email:", data["client_email"])

# Your Dialogflow Project ID
DIALOGFLOW_PROJECT_ID = "agentx-mhro"
SESSION_ID = "visitorz-chat-session"  # Can be anything (unique per user)


# with open("D:/Projects/ChatBot/agentx-mhro-a8846cad656d.json", "r") as file:
#     data = json.load(file)

# print("Project ID:", data.get("project_id"))
# print("Client Email:", data.get("client_email"))
# print("Private Key Exists:", "private_key" in data)



def get_dialogflow_response(text):
    """ Sends user input to Dialogflow and returns the response """
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

    text_input = dialogflow.TextInput(text=text, language_code="en")
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    return response.query_result.fulfillment_text  # Bot response


@app.post("/webhook")
async def chatbot_response(request: Request):
    data = await request.json()
    user_message = data.get("query", "")

    bot_response = get_dialogflow_response(user_message)  # Get response from Dialogflow

    return {"response": bot_response}
