import os
import subprocess
import sys
import gitlab

# Configuration
GITLAB_URL = 'https://gitlab.com'
GITLAB_PRIVATE_TOKEN = 'your_private_token'
GITLAB_GROUP_ID = 'your_group_id'  # Replace with your GitLab group ID

def create_local_project(project_name, file_type):
    os.makedirs(project_name, exist_ok=True)
    
    # Create a template file based on the specified file type
    file_content = {
        'c': '#include <stdio.h>\n\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}\n',
        'yaml': 'name: Hello World\nversion: 0.1.0\n',
        'python': 'print("Hello, World!")\n'
    }

    template_file = f'main.{file_type}'
    with open(os.path.join(project_name, template_file), 'w') as file:
        file.write(file_content.get(file_type, ''))

    # Initialize git repository
    subprocess.run(['git', 'init'], cwd=project_name)
    subprocess.run(['git', 'add', '.'], cwd=project_name)
    subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=project_name)
    print(f'Local project "{project_name}" created with a {file_type} template.')

def push_to_gitlab(project_name):
    gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_PRIVATE_TOKEN)
    group = gl.groups.get(GITLAB_GROUP_ID)

    project = gl.projects.create({'name': project_name, 'namespace_id': group.id})
    remote_url = project.ssh_url_to_repo

    # Add remote and push to GitLab
    subprocess.run(['git', 'remote', 'add', 'origin', remote_url], cwd=project_name)
    subprocess.run(['git', 'push', '-u', 'origin', 'master'], cwd=project_name)
    print(f'Project "{project_name}" pushed to GitLab.')

def open_in_vscode(project_name):
    subprocess.run(['code', project_name])
    print(f'Project "{project_name}" opened in VSCode.')

def main():
    if len(sys.argv) != 3:
        print('Usage: python new_project.py <project_name> <file_type>')
        sys.exit(1)

    project_name = sys.argv[1]
    file_type = sys.argv[2]

    create_local_project(project_name, file_type)
    push_to_gitlab(project_name)
    open_in_vscode(project_name)

if __name__ == '__main__':
    main()