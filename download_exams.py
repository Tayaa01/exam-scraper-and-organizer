import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import random

# Function to classify difficulty
def classify_difficulty():
    difficulty = random.choice(['easy', 'medium', 'hard'])
    return difficulty

# Retry mechanism with exponential backoff
retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session = requests.Session()
session.mount('https://', HTTPAdapter(max_retries=retries))

# Function to download exams based on URLs and subject
def download_exams(subject, quarters_urls, year_directory):
    # Iterate through each quarter URL
    for index, url in enumerate(quarters_urls, start=1):
        # Send an HTTP request to the website
        try:
            response = session.get(url, timeout=(3, 30))  # Increase timeout to 30 seconds (connect, read)

            # Check if the request was successful
            response.raise_for_status()

            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Define the base directory to save the downloaded exams
            base_download_directory = os.path.join(year_directory, subject, f'Quarter {index}')
            os.makedirs(base_download_directory, exist_ok=True)

            # Find all exam entries within table cells
            exam_entries = soup.find_all('td', class_='attachment-title')

            # Extract exam information and download links
            for entry in exam_entries:
                # Find the link and title
                link_tag = entry.find('a', class_='attachment-link')
                if link_tag:
                    title = link_tag.text.strip()
                    link = link_tag['href'].strip()

                    # Classify difficulty
                    difficulty = classify_difficulty()

                    # Create subfolder based on difficulty
                    download_directory = os.path.join(base_download_directory, difficulty)
                    os.makedirs(download_directory, exist_ok=True)

                    # Send a request to download the file
                    try:
                        file_response = session.get(link, timeout=(3, 30))  # Increased timeout for download
                        file_response.raise_for_status()  # Raise an exception for bad response status

                        # Clean the title to create a valid filename
                        filename = title.replace(' ', '_').replace('/', '_').replace('\\', '_') + '.pdf'
                        filepath = os.path.join(download_directory, filename)

                        # Save the file
                        try:
                            with open(filepath, 'wb') as file:
                                file.write(file_response.content)
                            print(f"Downloaded: {title} (Subject: {subject}, Difficulty: {difficulty})")
                        except Exception as e:
                            print(f"Failed to save {title}: {e}")
                    except requests.exceptions.RequestException as e:
                        print(f"Failed to download {title}: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {url}: {e}")

try:
    # Main directory for all exams within the user's home directory
    home_directory = os.path.expanduser('~')
    main_directory = os.path.join(home_directory, 'Exams')
    os.makedirs(main_directory, exist_ok=True)

    # URLs for exams
    years_urls = {
        'First Year': {
            'Mathematics': [
                'https://9raya.tn/إمتحانات-الرياضيات-الثلاثي-الأول/?_sft_category=اولى-اساسي&_sft_trimestre=الثلاثي-الأول&_sft_matiere=رياضيات',
                'https://9raya.tn/إمتحانات-رياضيات-الثلاثي-الثاني-2/?_sft_category=اولى-اساسي&_sft_trimestre=الثلاثي-الثاني&_sft_matiere=رياضيات',
                'https://9raya.tn/إمتحانات-رياضيات-الثلاثي-الثالث/?_sft_category=اولى-اساسي&_sft_trimestre=الثلاثي-الثالث&_sft_matiere=رياضيات'
            ],
            'Science': [
                'https://9raya.tn/إمتحانات-إيقاظ-علمي-الثلاثي-الأول-2/?_sft_category=اولى-اساسي&_sft_trimestre=الثلاثي-الأول&_sft_matiere=ايقاظ-علمي',
                'https://9raya.tn/إمتحانات-إيقاظ-علمي-الثلاثي-الثاني-2/?_sft_category=اولى-اساسي&_sft_trimestre=الثلاثي-الثاني&_sft_matiere=ايقاظ-علمي',
                'https://9raya.tn/إمتحانات-الايقاظ-العلمي-الثلاثي-الثا/?_sft_category=اولى-اساسي&_sft_trimestre=الثلاثي-الثالث&_sft_matiere=ايقاظ-علمي'
            ]
        },
        'Second Year': {
            'Mathematics': [
                'https://9raya.tn/امتحانات-في-الرياضيات-الثلاثي-الأول/?_sft_category=ثانية-اساسي&_sft_trimestre=الثلاثي-الأول&_sft_matiere=رياضيات',
                'https://9raya.tn/إمتحانات-رياضيات-الثلاثي-الثاني-3/?_sft_category=ثانية-اساسي&_sft_trimestre=الثلاثي-الثاني&_sft_matiere=رياضيات',
                'https://9raya.tn/إمتحانات-الرياضيات-الثلاثي-الثالث/?_sft_category=ثانية-اساسي&_sft_trimestre=الثلاثي-الثالث&_sft_matiere=رياضيات'
            ],
            'Science': [
                'https://9raya.tn/إمتحانات-الإيقاظ-العلمي-الثلاثي-الأو/?_sft_category=ثانية-اساسي&_sft_trimestre=الثلاثي-الأول&_sft_matiere=ايقاظ-علمي',
                'https://9raya.tn/السنة-الثانية-إمتحانات-الرياضيات-الث/?_sft_category=ثانية-اساسي&_sft_trimestre=الثلاثي-الثاني&_sft_matiere=ايقاظ-علمي',
                'https://9raya.tn/جديد-2019-إمتحان-إيقاظ-علمي-الثلاثي-الثال/?_sft_category=ثانية-اساسي&_sft_trimestre=الثلاثي-الثالث&_sft_matiere=ايقاظ-علمي'
            ]
        },
        'Third Year': {
            'Mathematics': [
                'https://9raya.tn/إمتحانات-رياضيات-الإصلاح/?_sft_category=ثالثة-اساسي&_sft_trimestre=الثلاثي-الأول&_sft_matiere=رياضيات',
                'https://9raya.tn/إمتحانات-رياضيات-الإصلاح-الثلاثي-الث/?_sft_category=ثالثة-اساسي&_sft_trimestre=الثلاثي-الثاني&_sft_matiere=رياضيات',
                'https://9raya.tn/إختبارات-رياضيات-الثلاثي-الثالث/?_sft_category=ثالثة-اساسي&_sft_trimestre=الثلاثي-الثالث&_sft_matiere=رياضيات'
            ],
            'Science': [
                'https://9raya.tn/إمتحانات-إيقاظ-علمي-مع-الإصلاح/?_sft_category=ثالثة-اساسي&_sft_trimestre=الثلاثي-الأول&_sft_matiere=ايقاظ-علمي',
                'https://9raya.tn/إمتحانات-إيقاظ-علمي-الإصلاح-الثلاثي/?_sft_category=ثالثة-اساسي&_sft_trimestre=الثلاثي-الثاني&_sft_matiere=ايقاظ-علمي',
                'https://9raya.tn/امتحانات-سنة-ثالثة-الثلاثي-الثالث/?_sft_category=ثالثة-اساسي&_sft_trimestre=الثلاثي-الثالث&_sft_matiere=ايقاظ-علمي'
            ],
            'French': [
                'https://9raya.tn/إمتحانات-فرنسية-جديد-الثلاثي-الأول/?_sft_category=ثالثة-اساسي&_sft_trimestre=الثلاثي-الأول&_sft_matiere=فرنسية',
                'https://9raya.tn/امتحانات-السنة-الثالثة-ابتدائي/?_sft_category=ثالثة-اساسي&_sft_trimestre=الثلاثي-الثاني&_sft_matiere=فرنسية',
                'https://9raya.tn/إمتحانات-الثلاثي-الثالث-في-اللغة-الفرنسية/?_sft_category=ثالثة-اساسي&_sft_trimestre=الثلاثي-الثالث&_sft_matiere=فرنسية'
            ]
        }
    }

    # Iterate through each year and subject, download exams
    for year, subjects in years_urls.items():
        year_directory = os.path.join(main_directory, year)
        os.makedirs(year_directory, exist_ok=True)
        for subject, urls in subjects.items():
            download_exams(subject, urls, year_directory)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    session.close()  # Close the session