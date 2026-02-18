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
        #frames
        self.variable_frame = ctk.CTkFrame(self.window, fg_color=("white", "#1e1e1e"), corner_radius=16, border_width=1, border_color="#333")
        self.variable_frame.grid(pady=10, padx=10, sticky="nsew", row=0, column=1)
        self.issue_selector_frame = ctk.CTkFrame(self.window, fg_color=("white", "#1e1e1e"), corner_radius=16, border_width=1, border_color="#333")
        self.issue_selector_frame.grid(pady=10, padx=10, sticky="nsew", row=0, column=2)
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
        self.name_entry = ctk.CTkEntry(self.variable_frame, placeholder_text="e.g. John",
                           placeholder_text_color="gray",
                           height=36, corner_radius=10, border_width=1)
        self.name_entry.grid(pady=5, padx=5, row=1, column=0, sticky="w")
        self.business_entry = ctk.CTkEntry(self.variable_frame, placeholder_text="e.g. John's Bakery",
                           placeholder_text_color="gray",
                           height=36, corner_radius=10, border_width=1)
        self.business_entry.grid (pady=5, padx=5, row=3, column=0, sticky="w")
        self.website_entry = ctk.CTkEntry(self.variable_frame, placeholder_text="e.g. https://example.com",
                           placeholder_text_color="gray",
                           height=36, corner_radius=10, border_width=1)
        self.website_entry.grid(pady=5, padx=5, row=5, column=0, sticky="ew")
        self.price_entry = ctk.CTkEntry(self.variable_frame, placeholder_text="Leave blank for auto-calculation",
                           placeholder_text_color="gray",
                           height=36, corner_radius=10, border_width=1)
        self.price_entry.grid(pady=10, padx=5, row=1, column=1, sticky="ew")
        self.timeframe_entry = ctk.CTkEntry(self.variable_frame, textvariable=self.timeframe_integer, placeholder_text="e.g. 2",
                           placeholder_text_color="gray",
                           height=36, corner_radius=10, border_width=1)
        self.timeframe_entry.grid(pady=5, padx=5, row=4, column=1, sticky="ew")
        #menus
        self.language_selector = ctk.CTkOptionMenu(self.variable_frame, values=["English", "Dutch", "French"],
                         corner_radius=10,
                         button_color="#2563eb", button_hover_color="#1d4ed8", fg_color="#2563eb"
                         )
        self.language_selector.grid(pady=10, padx=10, row=5, column=1, sticky="snew")
        self.message_type_selector = ctk.CTkOptionMenu(
            self.variable_frame,
            values=["Website Creation", "Website Fix", "Website Maintenance"],
                         corner_radius=10,
                         button_color="#2563eb", button_hover_color="#1d4ed8", fg_color="#2563eb"
        )
        self.message_type_selector.grid(pady=10, padx=10, row=7, column=0, sticky="w")
        self.timeframe_menu = ctk.CTkOptionMenu(
            self.variable_frame, values=["months", "weeks", "days"],
                         corner_radius=10,
                         button_color="#2563eb", button_hover_color="#1d4ed8", fg_color="#2563eb"
        )
        self.timeframe_menu.grid(pady=5, padx=5, row=3, column=1, sticky="snew")
        #labels
        self.email_label = ctk.CTkLabel(self.setup_frame, text="Enter Email Address:", font=ctk.CTkFont(size=20, weight="bold"),text_color=("black", "white"))
        self.email_label.grid(pady=10, padx=5, row = 0, column=0)
        self.auth_label = ctk.CTkLabel(self.setup_frame, text="Auth status:", font=ctk.CTkFont(size=20), text_color=("black", "white"))
        self.auth_label.grid(pady=(0, 10), padx=5, row=2, column=0, sticky= "snew")
        self.auth_status_label = ctk.CTkLabel(self.setup_frame, text="Not authenticated", font=ctk.CTkFont(size=15), text_color="red")
        self.auth_status_label.grid(pady=(0, 10), padx=5, row=3, column=0)
        self.namelabel = ctk.CTkLabel(self.variable_frame, text="Name:", font=ctk.CTkFont(size=15, weight="bold"), text_color=("black", "white"))
        self.namelabel.grid(pady=5, padx=5, row=0, column=0, sticky="ew")
        self.business_label = ctk.CTkLabel(self.variable_frame, text="Business Name:", font=ctk.CTkFont(size=15, weight="bold"), text_color=("black", "white"))
        self.business_label.grid(pady=5, padx=5, row=2, column=0, sticky="ew")
        self.timeframe_label = ctk.CTkLabel(self.variable_frame, text="Timeframe (number):", font=ctk.CTkFont(size=15, weight="bold"), text_color=("black", "white"))
        self.timeframe_label.grid(pady=5, padx=5, row=2, column=1, sticky="ew")
        self.website_label = ctk.CTkLabel(self.variable_frame, text="Website URL:", font=ctk.CTkFont(size=15, weight="bold"), text_color=("black", "white"))
        self.website_label.grid(pady=5, padx=5, row=4, column=0, sticky="ew")
        self.issue_label = ctk.CTkLabel(self.issue_selector_frame, text="Select Website Issue:", font=ctk.CTkFont(size=15, weight="bold"), text_color=("black", "white"))
        self.issue_label.grid(pady=5)
        self.price_label = ctk.CTkLabel(self.variable_frame, text="Set Price:", font=ctk.CTkFont(size=15, weight="bold"), text_color=("black", "white"))
        self.price_label.grid(pady=10, padx=5, row=0, column=1, sticky="ew")
        self.message_status_label = ctk.CTkLabel(self.window, text="")
        self.message_status_label.grid(pady=(0, 10), padx=10, row=4, column=1, columnspan=3, sticky="w")
        self.message_goal_label = ctk.CTkLabel(self.variable_frame, text="Message Goal:", font=ctk.CTkFont(size=15, weight="bold"), text_color=("black", "white"))
        self.message_goal_label.grid(pady=5, padx=10, row=6, column=0)
        self.issue_options = [
    "Slow loading times",
    "Not mobile-friendly",
    "Broken links or forms",
    "Outdated design",
    "Poor SEO performance",
     ]
        #checkboxes
        for option in self.issue_options:
           var = ctk.BooleanVar(value=False)
           self.issue_vars[option] = var
           cb = ctk.CTkCheckBox(self.issue_selector_frame, text=option, variable=var,
                     checkbox_width=18, checkbox_height=18,
                     corner_radius=4, fg_color="#2563eb", hover_color="#1d4ed8")
           cb.grid(pady=2, padx=5, sticky="w")
        # Initialize message variable
        self.message = ""
    def template_parse(self):
        if not Path("templates.json").exists():
            Path("templates.json").write_text(json.dumps({}))
        with open("templates.json", "r") as f:
            templates = json.load(f)
            var_list = list(templates.keys())
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
            # message['From'] = 'me'  
            message['Subject'] = 'Website Service Inquiry'
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
        selected_value = self.message_type_selector.get()
        name = self.name_entry.get()
        your_name = "Omar"
        contact = "Number: +32477091470 Email: wlamasat@gmail.com"
        if self.timeframe_integer.get() <= 0:
            self.message_status_label.configure(text="Please enter a valid timeframe number.", text_color="red")
            return
        else: timeframe = f"{self.timeframe_integer.get()} {self.timeframe_menu.get()}"
        your_site = "https://clearwebstudio.netlify.app/"
        website = self.website_entry.get().strip()
        selected_issues = [opt for opt, var in self.issue_vars.items() if var.get()]
        issue = ", ".join(selected_issues) if selected_issues else "various issues"
        price = 0
        if not self.business_entry.get():
            business = name
        else:
            business = self.business_entry.get()
        if  not self.price_entry.get():
            price = len(selected_issues) * 50 + 100
        else:
            price = self.price_entry.get()
        if self.language_selector.get() == "Dutch":
            if selected_value == "Website Creation":
                self.message = (
                    f"Dag {name},\nik ben {your_name}, een lokale webdeveloper.\n"
                    f"Ik zag dat {business} baat zou hebben bij een moderne website (of een upgrade van {website}).\n"
                    f"Ik kan een snelle, mobielvriendelijke site bouwen met het nodige: diensten, openingsuren, contact/boeken en basis SEO.\n"
                    f"Vaste prijs: €{price}. Oplevering: {timeframe}.\n"
                    f"Als je wil, stuur ik een kort plan + 2 designvoorbeelden door.\n"
                    f"Contact: {your_name} | {your_site} | {contact}.\n"
                )
            elif selected_value == "Website Fix":
                self.message = (
                    f"Dag {name},\nik ben {your_name}. Ik bekeek {website} en merkte: {issue}.\n"
                    f"Dat kan aanvragen/boekingen kosten, zeker op mobiel.\n"
                    f"Ik bied een snelle Website Fix + Speed Boost: mobiele layout fixes, kapotte links/formulieren herstellen en snelheid verbeteren.\n"
                    f"Vaste prijs: €{price}. Oplevering: {timeframe}.\n"
                    f"Wil je dat ik een korte checklist stuur met wat ik precies zou aanpakken.\n"
                    f"Contact: {your_name} | {your_site} | {contact}.\n"
                )
            elif selected_value == "Website Maintenance":
                self.message = (
                    f"Dag {name},\n{your_name} hier.\n"
                    f"Ik kan het website-onderhoud van {business} overnemen zodat alles snel, veilig en up-to-date blijft.\n"
                    f"Maandelijks onderhoud bevat: kleine aanpassingen, kapotte links/formulieren fixen, snelheidschecks en basis SEO-tweaks.\n"
                    f"Prijs per maand: €{price}.\n"
                    f"Zal ik even sturen wat ik precies voorstel voor jullie site ({website}).\n"
                    f"Contact: {your_name} | {your_site} | {contact}.\n"
                )
        elif self.language_selector.get() == "French":
            if selected_value == "Website Creation":
                self.message = (
                    f"Bonjour {name},\nje suis {your_name}, developpeur web dans la region.\n"
                    f"J'ai vu que {business} pourrait beneficier d'un site web moderne (ou d'une amelioration de {website}).\n"
                    f"Je peux creer un site rapide et adapte mobile avec l'essentiel : services, horaires, contact/reservation et bases SEO.\n"
                    f"Prix fixe : €{price}. Delai : {timeframe}.\n"
                    f"Si vous voulez, je peux envoyer un mini plan + 2 exemples de design.\n"
                    f"Contact: {your_name} | {your_site} | {contact}.\n"
                )
            elif selected_value == "Website Fix":
                self.message = (
                    f"Bonjour {name},\nje suis {your_name}. J'ai consulte {website} et j'ai remarque : {issue}.\n"
                    f"Cela peut faire perdre des demandes/reservations, surtout sur mobile.\n"
                    f"Je propose un Fix + Acceleration : corrections mobile, liens/formulaires, et amelioration de vitesse.\n"
                    f"Prix fixe : €{price}. Delai : {timeframe}.\n"
                    f"Souhaitez-vous que je vous envoie une courte checklist des points a corriger.\n"
                    f"Contact: {your_name} | {your_site} | {contact}.\n"
                )
            elif selected_value == "Website Maintenance":
                self.message = (
                    f"Bonjour {name},\n{your_name} ici.\n"
                    f"Je peux gerer la maintenance du site de {business} pour qu'il reste rapide, securise et a jour.\n"
                    f"La maintenance mensuelle comprend : petites mises a jour, corrections de liens/formulaires, verification de vitesse et ajustements SEO de base.\n"
                    f"Prix mensuel : €{price}.\n"
                    f"Souhaitez-vous que je vous envoie ce que j'inclurais pour votre site ({website}).\n"
                    f"Contact: {your_name} | {your_site} | {contact}.\n"
                )
        elif self.language_selector.get() == "English":
            if selected_value == "Website Creation":
                self.message = (
                    f"Hi {name},\nI'm {your_name}, a local web developer.\n"
                    f"I noticed {business} could benefit from a clean, modern website (or an upgrade of {website}).\n"
                    f"I can build a fast, mobile-friendly site with the essentials: services, opening hours, contact/booking, and SEO basics.\n"
                    f"Fixed price: €{price}. Estimated delivery: {timeframe}.\n"
                    f"If you'd like, I can send a simple plan + 2 design examples.\n"
                    f"Contact: {your_name} | {your_site} | {contact}.\n"
                )
            elif selected_value == "Website Fix":
                self.message = (
                    f"Hi {name},\nI'm {your_name}. I checked {website} and noticed: {issue}.\n"
                    f"This can cost you inquiries/bookings, especially on mobile.\n"
                    f"I offer a quick Website Fix + Speed Boost: mobile layout fixes, broken links/forms, and speed improvements.\n"
                    f"Fixed price: €{price}. Delivery: {timeframe}.\n"
                    f"Want me to send a short checklist of what I'd fix.\n"
                    f"Contact: {your_name} | {your_site} | {contact}.\n"
                )
            elif selected_value == "Website Maintenance":
                self.message = (
                    f"Hi {name},\n{your_name} here.\n"
                    f"I can take care of website maintenance for {business} so everything stays fast, secure, and up to date.\n"
                    f"Monthly maintenance includes: small content updates, fixing broken links/forms, speed checks, and basic SEO tweaks.\n"
                    f"Monthly price: €{price}.\n"
                    f"Want me to send what I'd include for your site ({website}).\n"
                    f"Contact: {your_name} | {your_site} | {contact}.\n"
                )
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
