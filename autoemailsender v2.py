import customtkinter as ctk
import base64
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from pathlib import Path
from google.auth.transport.requests import Request
from quickstart import main as authenticate_gmail
import json
class Emailsender:
    def __init__(self):
        # Set up the main application window
        ctk.set_appearance_mode("dark")      
        ctk.set_default_color_theme("dark-blue")  
        self.window = ctk.CTk()
        self.window.title("Automated Email Sender")
        for i in range(4):
            self.window.grid_columnconfigure(i, weight=1)
            self.window.grid_rowconfigure(0, weight=1)
        self.template_parse()
        #frames
        self.variable_frame = ctk.CTkFrame(self.window, fg_color=("white", "#1e1e1e"), corner_radius=16, border_width=1, border_color="#333")
        self.variable_frame.grid(pady=10, padx=10, sticky="nsew", row=0, column=1)
        self.message_textbox = ctk.CTkTextbox(self.window, width=400, height=200, corner_radius=12, border_width=1, border_color="#333")
        self.message_textbox.grid(pady=10, padx=10, row=2, column=1, columnspan=3, sticky="nsew")
        self.message_textbox.configure(state="disabled")
        self.setup_frame = ctk.CTkFrame(self.window, fg_color=("white", "#1e1e1e"), corner_radius=16, border_width=1, border_color="#333")
        self.setup_frame.grid(pady=10, padx=10, sticky="nsew", row=0, column=0, columnspan=1)
        #variables
        self.timeframe_integer = ctk.IntVar()
        self.issue_vars = {}  
        self.auth_var = ctk.BooleanVar(value=False)
        #buttons
        self.auth_button = ctk.CTkButton(
            self.setup_frame, text="Authenticate", command=self.authenticate,
                          height=42, corner_radius=12,
                         fg_color="#2563eb", hover_color="#1d4ed8",
                         font=ctk.CTkFont(size=14, weight="bold")
        )
        self.auth_button.grid(pady=10, padx=5, row=4, column=0, sticky="ew")
        self.msg_generate_button = ctk.CTkButton(
            self.window, text="Generate Message", command=lambda: self.message_setup(),
                          height=42, corner_radius=12,
                         fg_color="#2563eb", hover_color="#1d4ed8",
                         font=ctk.CTkFont(size=14, weight="bold")
        )
        self.msg_generate_button.grid(pady=10, padx=10, row=3, column=1, columnspan=3, sticky="ew")
        self.message_button = ctk.CTkButton(
            self.window, text="Send Email", command=self.API_setup,
                          height=42, corner_radius=12,
                         fg_color="#2563eb", hover_color="#1d4ed8",
                         font=ctk.CTkFont(size=14, weight="bold")
        )
        self.message_button.grid(pady=10, padx=10, row=6, column=0, columnspan=3, sticky="ew")
        self.message_button.configure(state="disabled")
        #entries
        self.email_entry = ctk.CTkEntry(self.setup_frame, placeholder_text="name@business.com",
                           placeholder_text_color="gray",
                           height=36, corner_radius=10, border_width=1)
        self.email_entry.grid(pady=10, padx=5, row=1, column=0, sticky="ew")
        #menus
        self.menu_list = []
        for i, param in enumerate(self.param_list):
            if param[0] == 'subject':
                del param[0]
            param_menu = ctk.CTkOptionMenu(self.variable_frame, values=param,
                         corner_radius=10,
                         button_color="#2563eb", button_hover_color="#1d4ed8", fg_color="#2563eb",
                         )
            param_menu.grid(pady=5, padx=5, row=0+i, column=0, sticky="ew")
            self.menu_list.append(param_menu)
        #labels
        self.email_label = ctk.CTkLabel(self.setup_frame, text="Enter Email Address:", font=ctk.CTkFont(size=20, weight="bold"),text_color=("black", "white"))
        self.email_label.grid(pady=10, padx=5, row = 0, column=0)
        self.auth_label = ctk.CTkLabel(self.setup_frame, text="Auth status:", font=ctk.CTkFont(size=20), text_color=("black", "white"))
        self.auth_label.grid(pady=(0, 10), padx=5, row=2, column=0, sticky= "snew")
        self.auth_status_label = ctk.CTkLabel(self.setup_frame, text="Not authenticated", font=ctk.CTkFont(size=15), text_color="red")
        self.auth_status_label.grid(pady=(0, 10), padx=5, row=3, column=0)
        self.message_status_label = ctk.CTkLabel(self.window, text="")
        self.message_status_label.grid(pady=(0, 10), padx=10, row=4, column=1, columnspan=3, sticky="w")
        self.message = ""
    def template_parse(self):
        if not Path("templates.json").exists():
            Path("templates.json").write_text(json.dumps({}))
        self.param_list =[]
        with open("templates.json", "r") as f:
            templates = json.load(f)
        self.message_template = templates
        current = templates
        while isinstance(current, dict) and current:
             keys = list(current.keys())       
             self.param_list.append(keys)       
             first_key = keys[0]               
             current = current[first_key]       
    def authenticate(self):
        SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        self.creds = None
        if Path("token.json").exists():
            self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
                Path("token.json").write_text(self.creds.to_json())
            self.auth_status_label.configure(text="Authenticated", text_color="green")
            self.auth_var.set(True)
        else:
            authenticate_gmail()
            if Path("token.json").exists():
                self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)
                self.auth_status_label.configure(text="Authenticated", text_color="green")
    def API_setup(self):
        if not self.auth_var.get():
            self.message_status_label.configure(text="Please authenticate first.", text_color="red")
            return
        if not "@" in self.email_entry.get().strip() or not "." in self.email_entry.get().strip():
            self.message_status_label.configure(text="Please enter a valid email address.", text_color="red")
            return
        try:
        # 1. Create the email structure
            service = build('gmail', 'v1', credentials=self.creds)
            message = EmailMessage()
            if self.message == "":
                return
            message.set_content(self.message)
            message['To'] = self.email_entry.get() 
            message['Subject'] = self.subject
        # 2. Encode the message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            create_message = {
              'raw': encoded_message
            }
            send_request = service.users().messages().send(userId="me", body=create_message)
            sent_message = send_request.execute()
        
            self.message_status_label.configure(text="Email sent successfully!", text_color="green")

        except HttpError as error:
            print(f'An error occurred: {error}')
            self.message_status_label.configure(text="Error sending email.", text_color="red")
            sent_message = None
        finally:
            self.message = ""
            self.message_textbox.configure(state="normal")
            self.message_textbox.delete("1.0", "end")
            self.message_textbox.configure(state="disabled")
            self.email_entry.delete(0, "end")

        return sent_message
    def message_setup(self):
        current = self.message_template
        current_subject = self.message_template
        for menu in self.menu_list:
            current = current[menu.get()]
        for menu in self.menu_list:
            if menu.get() == 'subject' or menu.get() == 'body':
                current_subject = current_subject['subject']
                break
            current_subject = current_subject[menu.get()]
        self.message = current
        self.subject = current_subject
        self.message_textbox.configure(state="normal")
        self.message_status_label.configure(text="Message generated! Review and click 'Send Email'.", text_color="green")
        self.message_textbox.delete("1.0", "end")
        self.message_textbox.insert("1.0", self.message)
        self.message_button.configure(state="normal")
        self.message_textbox.configure(state="disabled")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = Emailsender()
    app.run()
