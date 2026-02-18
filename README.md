# Auto-email-sending-app
A Python desktop application built with CustomTkinter that allows users to generate and send structured email templates using the Gmail API.

This project is currently evolving toward a more advanced automated bulk email system where users will be able to:

Send emails to multiple recipients

Create and manage custom templates

Use dynamic variables (e.g. {name}, {business}, {website})

Fully customize message structures via JSON templates

Automate structured outreach campaigns

🚀 Current Features

Gmail API integration (OAuth 2.0)

Token auto-refresh handling

Multi-language template support (English / Dutch / French)

Dynamic template selection via JSON

Variable-based message generation

GUI built with CustomTkinter

Form validation

Clean dark-themed UI

🛠️ Tech Stack

Python 3

CustomTkinter (GUI)

Google Gmail API

OAuth 2.0 authentication

JSON-based template management

Git for version control

📂 Project Structure
Auto-email-sending-app/
│
├── main.py
├── templates.json          (going to be added in future updates)
├── credentials.json        (not included in repo)
├── token.json              (generated locally)
├── README.md
└── .gitignore

🔐 Setup Instructions
1️⃣ Clone the repository
git clone https://github.com/TheKingOmar/Auto-email-sending-app.git
cd Auto-email-sending-app

2️⃣ Install dependencies
pip install customtkinter google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

3️⃣ Set up Google API Credentials

Go to Google Cloud Console

Create a new project

Enable Gmail API

Create OAuth 2.0 Desktop credentials

Download the file and rename it to:

credentials.json


Place it in the project root.

⚠️ Do NOT commit credentials.json or token.json to GitHub.

🧠 How Templates Work

Templates are stored inside templates.json.

Example structure:

{
  "English": {
    "Website Creation": {
      "subject": "Website Service Inquiry",
      "body": "Hi {name}, I noticed {business} could benefit from..."
    }
  }
}


The app dynamically parses this structure and generates dropdown menus based on the nesting level.

Future versions will allow:

Template editing inside the GUI

Parameter auto-detection

Variable mapping system

Campaign-style multi-recipient sending

🔮 Roadmap

 Editable templates inside the app

 Bulk email sending from CSV

 Variable auto-detection {variable}

 Email preview mode

 Campaign tracking

 Improved UI layout system

 Error logging system

 Packaging into executable (.exe)

📌 Future Vision

This project is developing into a lightweight automated outreach tool that enables structured, customizable email campaigns without relying on third-party SaaS platforms.

The long-term goal is to build:

A customizable automail engine

Dynamic variable injection system

Scalable multi-recipient sending

Template-driven communication workflows


