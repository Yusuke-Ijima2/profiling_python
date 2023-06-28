import requests
import random
import os
import time

access_token = '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'
headers = {'Authorization': f'token {access_token}'}
minimum_lines = 100  # Minimum number of lines
maximum_lines = 200  # Maximum number of lines
directory = '/Users/iijimayuusuke/Profile_yusuke_ijima/ast/list_comprehension/before/analysis/test_code'
num_files_needed = 50
delay_between_requests = 5  # delay in seconds

num_files_found = 0

while num_files_found < num_files_needed:
    while True:
        response = requests.get(
            'https://api.github.com/search/repositories?q=language:python', headers=headers)

        print(response)

        if response.status_code != 200:
            # API request was not successful
            raise Exception(
                f'Request failed with status {response.status_code}')

        # Get the JSON response body
        data = response.json()

        # Get the list of repositories
        repos = data['items']

        # Choose a random repository
        repo = random.choice(repos)

        # Get the owner and name of the repository
        owner = repo['owner']['login']
        name = repo['name']

        response = requests.get(
            f'https://api.github.com/search/code?q=extension:py+repo:{owner}/{name}', headers=headers)

        if response.status_code != 200:
            # API request was not successful
            raise Exception(
                f'Request failed with status {response.status_code}')

        # Get the JSON response body
        data = response.json()

        # Get the list of files
        files = data['items']

        if files:
            break
        else:
            time.sleep(delay_between_requests)

    # Choose a random Python file
    file = random.choice(files)

    # Get the path of the file
    path = file['path']

    # Construct the raw URL
    raw_url = f'https://raw.githubusercontent.com/{owner}/{name}/master/{path}'

    # Download the file content
    response = requests.get(raw_url)

    # The content of the file is the response text
    content = response.text

    # Count the number of lines in the file
    num_lines = len(content.split('\n'))

    if minimum_lines <= num_lines <= maximum_lines:
        # If the file has an acceptable number of lines, save it to a file
        with open(os.path.join(directory, f'github_sample_{num_files_found + 1}.py'), 'w') as f:
            f.write(content)

        num_files_found += 1

    # Delay between requests
    time.sleep(delay_between_requests)
