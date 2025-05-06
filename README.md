# Worksy

An AI-powered job portal that connects job seekers with employers using advanced matching algorithms and OpenAI integration.

## Features

### For Job Seekers
- Browse and apply to jobs
- Get AI-powered job recommendations
- Track your applications and interviews
- AI resume assistant powered by OpenAI
- Skills analysis and development suggestions
- Messaging system to connect with recruiters

### For Recruiters
- Post and manage job listings
- Review applications
- Schedule interviews
- Find qualified candidates
- Message applicants

## Technology Stack

- **Backend**: Django 4.2
- **Frontend**: Bootstrap 5, HTML, CSS, JavaScript
- **Database**: PostgreSQL (production), SQLite (development)
- **AI/ML**: scikit-learn, NLTK, OpenAI
- **Authentication**: django-allauth with social authentication
- **Deployment**: Gunicorn, Whitenoise, Docker

## Installation

### Prerequisites
- Python 3.10+
- pip
- virtualenv (recommended)
- PostgreSQL (for production)

### Setup

1. Clone the repository:

###For Setting Up on new Device

1. Create venv then activate it
2. pip install django-environ
3. pip install -r requirements.txt
4. migrate and runserver if error persist saying "punkt"
5. Open python shell in vscode
6. import nltk - type this in shell
7. nltk.download('punkt', download_dir='/Users/judeibardaloza/  nltk_data') # the make sure to path it correctly if it is correct it will display nltk = True
8. Go to services.py under ai_matching and paste this code 
 Add the custom NLTK data path
nltk.data.path.append('/Users/judeibardaloza/Documents/nltk_data')

def ensure_nltk_data():
    """Ensure all required NLTK data is downloaded."""
    nltk_data_dir = '/Users/judeibardaloza/Documents/nltk_data'
    nltk.data.path.append(nltk_data_dir)  
    os.makedirs(nltk_data_dir, exist_ok=True)
    
    required_packages = ['punkt', 'stopwords']
    for package in required_packages:
        try:
            nltk.data.find(f'tokenizers/{package}')
        except LookupError:
            nltk.download(package, download_dir=nltk_data_dir)

9. pip install six and upgrade pip as well to avoid error 
10. runserver
