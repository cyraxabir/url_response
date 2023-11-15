import re
import request
from urllib.parse import urlparse, urlunparse
# Change this to the path of your output file
output_file_path = "url_dir.txt"
# Change this to the path where you want to save the URLs with successful responses
success_file_path = "got_response.txt"

def extract_urls(file_content):
    # Regular expression to match URLs
    url_pattern = re.compile(r'https?://[^\s]+')

    # Find all matches in the content
    urls = re.findall(url_pattern, file_content)
    
    return urls

def read_dirb_output(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_url_response(url):
    try:
        response = requests.get(url)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error making request to {url}: {e}")
        return None

def save_successful_urls(success_file, url):
    with open(success_file, 'a') as file:
        file.write(url + '\n')

def remove_trailing_slash(url):
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.rstrip('/').split('/')
    path_segments[-1] = path_segments[-1].rstrip('/')
    new_path = '/'.join(path_segments)
    
    modified_url = urlunparse(parsed_url._replace(path=new_path))
    return modified_url

def main():
    dirb_output = read_dirb_output(output_file_path)
    
    if dirb_output:
        urls = extract_urls(dirb_output)
        
        if urls:
            print("Fetching responses for URLs:")
            for url in urls:
                # Remove trailing slash from the last path segment
                modified_url = remove_trailing_slash(url)
                print(f"\nURL: {modified_url}")
                
                # Fetch response for each URL
                response = get_url_response(modified_url)
                
                if response:
                    print(f"Response Code: {response.status_code}")
                    #print("Response Content:")
                    #print(response.text[:300])  # Print the first 300 characters of the response content
                    
                    # Save URL to success_file if response is successful (e.g., status code 200)
                    if response.ok:
                        save_successful_urls(success_file_path, modified_url)
                else:
                    print("Failed to fetch response.")
        else:
            print("No URLs found in the output file.")

if __name__ == "__main__":
    main()

