import gspread
from oauth2client.service_account import ServiceAccountCredentials
import gitlab

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/ziv/git/ziv.gliser/devops/Python-Scripts/devops-infinity-676dbe238077.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open('Employee Information').sheet1

# Get all records from the sheet
records = sheet.get_all_records()

# GitLab setup
gl = gitlab.Gitlab('http://51.44.41.112', private_token='glpat-mseNJyzKx6HteL78ayUC')

# Main group ID where users will be added and repositories created
main_group_id = 6

for record in records:
    # Extract relevant information from the sheet
    name = record['name']
    email = record['email']
    username = record['username']
    password = 'Aa123456'  # Set a default password or generate one

    # Create a new user in GitLab
    user = gl.users.create({
        'email': email,
        'password': password,
        'username': username,
        'name': name,
        'skip_confirmation': True
    })

    # Get the main group
    group = gl.groups.get(main_group_id)

    # Add the user to the main group with the 'Reporter' role
    group.members.create({'user_id': user.id, 'access_level': 20})

    # Create a new project/repository for the user
    project = gl.projects.create({
        'name': username,
        'namespace_id': main_group_id
    })

    print(f'Created user {name} with username {username} and a repository named {username}.')
