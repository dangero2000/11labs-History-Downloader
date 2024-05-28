import requests
import os
import argparse
import re
from datetime import datetime
import csv

# Constants
MAX_ROWS_PER_FILE = 100

# Function to sanitize filenames
def sanitize_filename(filename):
    filename = re.sub(r'[\\/*?:"<>|]', '_', filename)
    filename = re.sub(r'[^a-zA-Z0-9_]', '', filename)
    return filename[:20]

# Function to convert Unix timestamp to readable date
def convert_unix_to_date(unix_timestamp):
    return datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d')

# Function to load existing CSV records into a set
def load_existing_records():
    existing_records = set()
    file_index = 1
    while os.path.exists(f'clip_records_{file_index}.csv'):
        with open(f'clip_records_{file_index}.csv', 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Skip header
            for row in csvreader:
                existing_records.add((row[0], row[1], row[2]))
        file_index += 1
    return existing_records

# Function to write a record to the CSV file
def write_record_to_csv(clip_name, clip_date, voice_name, file_path):
    file_index = 1
    while True:
        csv_file_name = f'clip_records_{file_index}.csv'
        if os.path.exists(csv_file_name):
            with open(csv_file_name, 'r', encoding='utf-8') as csvfile:
                row_count = sum(1 for row in csvfile)
            if row_count < MAX_ROWS_PER_FILE + 1:  # +1 for header row
                with open(csv_file_name, 'a', newline='', encoding='utf-8') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow([clip_name, clip_date, voice_name, file_path])
                return
        else:
            with open(csv_file_name, 'w', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['Clip Text', 'Clip Date', 'Voice Name', 'File Path'])
                csvwriter.writerow([clip_name, clip_date, voice_name, file_path])
            return
        file_index += 1

# Function to download a clip using the constructed URL
def download_clip(api_key, history_item_id, clip_name, clip_date, voice_name):
    base_url = 'https://api.elevenlabs.io/v1/'
    headers = {
        'xi-api-key': api_key,
        'Content-Type': 'application/json'
    }
    clip_url = f'{base_url}history/{history_item_id}/audio'
    try:
        response = requests.get(clip_url, headers=headers, stream=True)
        print(f"Download Request URL: {response.url}")
        print(f"Download Response Status Code: {response.status_code}")
        response.raise_for_status()

        if 'audio' not in response.headers.get('Content-Type', ''):
            print(f"Error: The response is not an audio file.")
            return

        # Create voice folder if it doesn't exist
        voice_folder = sanitize_filename(voice_name)
        if not os.path.exists(voice_folder):
            os.makedirs(voice_folder)

        # Sanitize the filename and include the date
        safe_filename = f"11labs_{clip_date}_{sanitize_filename(clip_name)}.mp3"
        file_path = os.path.join(voice_folder, safe_filename)

        # Check if the file already exists
        if os.path.exists(file_path):
            print(f"Skipping download: {file_path} already exists.")
            write_record_to_csv(clip_name, clip_date, voice_name, file_path)
            return file_path

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f'Downloaded: {file_path}')
        write_record_to_csv(clip_name, clip_date, voice_name, file_path)
        return file_path
    except OSError as os_error:
        print(f'OSError: {os_error}')
    except requests.exceptions.RequestException as e:
        print(f'Error downloading clip {clip_url}: {e}')
    return None

# Function to get all pages of history items and process each page immediately
def get_and_process_all_clips(api_key):
    base_url = 'https://api.elevenlabs.io/v1/'
    headers = {
        'xi-api-key': api_key,
        'Content-Type': 'application/json'
    }
    page = 1
    processed_files = 0

    # Load existing records to avoid duplicates
    existing_records = load_existing_records()

    while True:
        url = f'{base_url}history?page={page}'
        try:
            print(f"Making request to {url} with API key: {api_key}")
            response = requests.get(url, headers=headers)
            print(f"Request URL: {response.url}")
            print(f"Response Status Code: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            page_clips = data.get('history', [])
            if not page_clips:
                break
            
            # Process each clip immediately
            for clip in page_clips:
                print(f"Clip data: {clip}")
                history_item_id = clip.get('history_item_id', '')
                clip_name = clip.get('text', 'unnamed_clip')
                clip_date = convert_unix_to_date(clip.get('date_unix', 0))
                voice_name = clip.get('voice_name', 'unknown_voice')
                if history_item_id:
                    if (clip_name, clip_date, voice_name) not in existing_records:
                        download_clip(api_key, history_item_id, clip_name, clip_date, voice_name)
                        existing_records.add((clip_name, clip_date, voice_name))
                    else:
                        print(f"Skipping record: {clip_name} on {clip_date} with voice {voice_name} already exists in CSV.")
                    processed_files += 1
                    if processed_files == 10:
                        if not user_confirmation("First 10 files processed. Do you want to continue? (Y/N): "):
                            return
                else:
                    print(f"Missing history_item_id for clip: {clip}")
                    if not user_confirmation():
                        return
            
            page += 1
        except requests.exceptions.RequestException as e:
            print(f'Error fetching clips: {e}')
            if not user_confirmation():
                return

    print(f"Finished processing all pages. Last page processed: {page - 1}")

# Function to ask for user confirmation
def user_confirmation(prompt="An error occurred. Do you want to continue? (Y/N): "):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in ['y', 'n']:
            return user_input == 'y'

# Main script
def main(api_key):
    os.makedirs('downloads', exist_ok=True)
    os.chdir('downloads')
    
    generate_csv = user_confirmation("Do you want to generate CSV records? (Y/N): ")
    get_and_process_all_clips(api_key)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download Eleven Labs clips.")
    parser.add_argument('--api_key', type=str, help='API key for Eleven Labs')
    args = parser.parse_args()

    if args.api_key:
        api_key = args.api_key
    else:
        api_key = input("Enter your Eleven Labs API key: ")

    print(f"Using API key: {api_key}")
    main(api_key)
