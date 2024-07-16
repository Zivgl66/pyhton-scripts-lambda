import gspread
from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest import Client

# Define the scope for Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Credentials for Google Sheets
creds = ServiceAccountCredentials.from_json_keyfile_name("path_to_your_credentials.json", scope)
client = gspread.authorize(creds)

# Open your Google Sheet by name
sheet = client.open("Your Google Sheet Name").sheet1

# Get all records from the sheet
contacts = sheet.get_all_records()

# Twilio credentials
twilio_account_sid = "your_twilio_account_sid"
twilio_auth_token = "your_twilio_auth_token"
twilio_whatsapp_number = "whatsapp:+14155238886"  # This is the Twilio sandbox number

# Initialize Twilio Client
twilio_client = Client(twilio_account_sid, twilio_auth_token)

# Predefined message
message_template = "Hello {name}, this is a predefined message."

# Function to send WhatsApp message
def send_whatsapp_message(to, body):
    message = twilio_client.messages.create(
        body=body,
        from_=twilio_whatsapp_number,
        to=f"whatsapp:{to}"
    )
    return message.sid

# Send messages to all contacts
for contact in contacts:
    name = contact['Name']
    phone_number = contact['Phone Number']
    personalized_message = message_template.format(name=name)
    message_sid = send_whatsapp_message(phone_number, personalized_message)
    print(f"Message sent to {name} ({phone_number}) with SID: {message_sid}")