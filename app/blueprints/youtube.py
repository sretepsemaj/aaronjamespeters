from flask import Blueprint, jsonify, render_template
from pytube import YouTube
import logging
from urllib.parse import urlparse, parse_qs
import requests

bp = Blueprint('youtube', __name__, url_prefix='/youtube')
logger = logging.getLogger(__name__)

def extract_video_id(url):
    """Extract video ID from any YouTube URL format."""
    try:
        # Handle youtu.be format
        if 'youtu.be' in url:
            return url.split('/')[-1].split('?')[0]
        
        # Handle youtube.com format
        parsed_url = urlparse(url)
        if 'youtube.com' in parsed_url.netloc:
            query_params = parse_qs(parsed_url.query)
            if 'v' in query_params:
                return query_params['v'][0]
        
        logger.debug(f"Extracted video ID from URL: {url}")
        return url
    except Exception as e:
        logger.error(f"Error extracting video ID from URL {url}: {str(e)}")
        return url

def get_best_thumbnail(video_id):
    """Get the best available thumbnail URL for a video."""
    # Try thumbnail qualities in order of preference
    qualities = ['maxresdefault', 'sddefault', 'hqdefault', 'mqdefault', 'default']
    
    for quality in qualities:
        url = f"https://img.youtube.com/vi/{video_id}/{quality}.jpg"
        try:
            response = requests.head(url)
            if response.status_code == 200:
                logger.debug(f"Found working thumbnail at quality: {quality}")
                return url
        except Exception as e:
            logger.debug(f"Error checking thumbnail at quality {quality}: {str(e)}")
            continue
    
    # If no thumbnails work, return the most reliable one
    return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

@bp.route('/')
def index():
    """YouTube gallery page route"""
    return render_template('youtube/index.html', title='YouTube Gallery')

@bp.route('/api/videos')
def get_videos():
    try:
        videos_data = [
            {
                'url': 'https://youtu.be/9Isksd9Xhqc',
                'title': 'WINDSURF - Making a FLASK APP EASY!!! - Initial Folder Structure and SETUP (VIDEO 1)',
                'description': '''Doing the first initial folder structure explanation and how to set up an easy PYTHON Flask app with WINDSURF code editor and codium AI or as I like to call it Cassi. This video starts the project of me setting up a work application demo page that I will use to apply to jobs. This is a series of videos where you can follow along to make your own app I'm going to demonstrate all the important things to consider when building a PYTHON Flask app.'''
            },
            {
                'url': 'https://youtu.be/Z1PDkh7eLss',
                'title': 'WINDSURF - Making a FLASK APP EASY!!! - Finishing folder structure (VIDEO 2)',
                'description': '''In this video, I demonstrate how WINDSURF editor and Codeium AI collaborate to generate a portion of the folder structure for a Flask app. Since Codeium can't generate the entire Flask application in one go, I walk you through what it successfully generated, how far it got, and how much more is required for the app to run locally in the browser. This highlights the gaps and the additional steps needed to complete the setup.'''
            },
            {
                'url': 'https://youtu.be/h3t_fyDctRI',
                'title': 'WINDSURF - Making a FLASK APP EASY!!! - Setting up the .venv folder  (VIDEO 3)',
                'description': '''In this video, I set up the .venv folder and ensure all dependencies are installed. I run into a few issues that require troubleshooting before successfully launching it in the browser in the next video. One key tip: when working in local development, avoid using HTTPS—it can clutter your terminal output and make it difficult to read.'''
            },
            {
                'url': 'https://youtu.be/XzVfzhoh4ZM',
                'title': 'WINDSURF - Making a FLASK APP EASY!!! - Troubleshooting/Debugging (VIDEO 4)',
                'description': '''In this video, watch me coach Cassi (Codeium AI) as it tries to render the initial setup of the Flask app. It's a bit of a struggle, and I make a few simple mistakes along the way, but in the end, I get the app up and running. A reminder that coding is all about persistence and learning from those small errors!'''
            },
            {
                'url': 'https://youtu.be/-dz2aCUmSCU',
                'title': 'WINDSURF - Making a FLASK APP EASY!!! - FORGOT!!! git init (VIDEO 5)',
                'description': '''In this video, I initialize Git and start tracking the project folder—something I really should have done from the start! Luckily, with WINDSURF editor and Codeium AI, getting everything set up correctly was quick and easy. I also create a dev branch and begin working from there, following best practices for development.'''
            },
            {
                'url': 'https://youtu.be/AmKMk8QW2x4',
                'title': 'WINDSURF - Making a FLASK APP EASY!!! - Different Logging Levels w/ quick chat (VIDEO 6)',
                'description': '''In this video, I walk through setting up logging for both development and production using WINDSURF editor chat. The goal is to configure logging so development has detailed local debugging, while production only tracks error and info logs. This setup makes it much easier to debug locally and monitor server-side activity. It also helps identify any unusual behavior from users, keeping the app secure and running smoothly.'''
            },
            {
                'url': 'https://youtu.be/zD2ilvrNGKc',
                'title': 'WINDSURF - Making a FLASK APP EASY!!! - DEBUG, DEBUG, DEBUG-.env creation & more DEBUGGING (VIDEO 7)',
                'description': '''In this video, I run into some challenges setting up proper logging. I create the essential .env file, but I struggle to get the logging configuration to work seamlessly between the .env, base.py, and its dependent configuration files—dev.py for local development and prod.py for deployment. I also go over how I set up the .env file to manage the environment for each configuration, ensuring that dev.py is used for local development and prod.py is ready for deployment. It's a great reminder that fine-tuning these configurations takes time but is crucial for a smooth development workflow.'''
            },
            {
                'url': 'https://youtu.be/059nc8wiXaw',
                'title': 'WINDSURF - Making a FLASK APP EASY!!! - Explainer of off Camera Logging Setup (VIDEO 8)',
                'description': '''In this video, I recap all the off-camera debugging and setup required to get the logging flow working properly. I couldn't show every step, but the key challenge was configuring the .env file to work seamlessly with .env.development and .env.production. These files connect through base.py in the config folder to ensure the right logging settings are applied from dev.py for development and prod.py for production. Since .env.production needs a secure token (secrets.token_hex(32)), I created a .env.production.template file to show the structure without exposing sensitive info. When deploying to Render, I'll generate the token and copy it into the actual .env.production file.'''
            },
            {
                'url': 'https://youtu.be/-bT9eOCnZMU',
                'title': 'WINDSURF - Making a FLASK APP EASY!!! - Git commit & Merge code back to main repo (VIDEO 9)',
                'description': '''In this video, I waited way too long to initialize Git, so it's time to fix that. I set up Git, make a dev commit, and since I didn't add a .gitignore or .gitkeep earlier, things got a little messy. Most of the video is me coaching back and forth to handle the merge and get everything from dev merged cleanly back into the main branch. Lesson learned—always set up Git and .gitignore early!'''
            },
            {
                'url': 'https://youtu.be/WAwTQDMVD7U',
                'title': 'WINDSURF - Making a FLASK APP EASY!!! - Add the Projects and YouTube buttons to home (VIDEO 10)',
                'description': '''In this video, I add Projects and YouTube buttons to the app to better showcase my skills. I decided to use Flask Blueprints to keep things professional. While I could've stuck with a single routes.py, breaking the logic into separate files using Blueprints makes the code much easier to navigate. It also simplifies debugging and updating the relationships between templates and endpoints. Definitely worth the extra effort!'''
            },
            {
                'url': 'https://youtu.be/P_MGzQJflQk',
                'title': 'WINDSURF - Making a FLASK APP EASY!!! Quick git commit & MAJOR HOME PAGE BUTTONS DEBUG (VIDEO 11)',
                'description': '''In this video, I do a quick commit and set up the Blueprint folder. Although I didn't get the app fully working at first, I realized off-camera that each Blueprint needs its own folder in the templates directory. Since it's my first time using Blueprints for script communication, there was definitely a learning curve. Thankfully, with the help of WINDSURF editor and Cassi (Codeium AI), we worked through it together. I'll explain how it all comes together in the next video!'''
            },
            {
                'url': 'https://youtu.be/m8ZRPhrVzy8',
                'title': 'WINDSURF - Making a FLASK APP EASY!!! Final Home Buttons FIX (VIDEO 12)',
                'description': '''In this video, I troubleshoot the templates folder setup. I had to create a separate folder for each Blueprint in the templates directory to render individual index.html files. This ensures that each endpoint has its own dedicated page, keeping everything organized and working as expected.'''
            },
            {
                'url': 'https://youtu.be/8vKqv_uPbEY',
                'title': 'WINDSURF - Making a FLASK APP EASY!!! Git commit & Logs BROKE had to debug them (VIDEO 13)',
                'description': '''In this video, I do a quick Git commit and then notice my logs have stopped working. Logs are essential—especially when using an AI code editor like WINDSURF or any other tool. While you can rely on the terminal in local development, once the app is deployed, there's no terminal access. Having info.log and error.log functioning correctly is crucial for tracking issues. It took some time to fix, but I made sure the terminal now displays the current environment so I don't accidentally work in the wrong one.'''
            },
            {
                'url': 'https://youtu.be/K_ND3X8UmAg',
                'title': 'WINDSURF - Making a FLASK APP EASY!!! STARTING TO ACTUALLY BUILD!!! (VIDEO 14)',
                'description': '''In this video, I start building the resume endpoint and make another Git commit. To help Cassi (Codeium AI) understand the structure of my resume, I used all caps for section headers.'''
            },
            {
                'url': 'https://youtu.be/3zQvQ7ZzQ8k',
                'title': 'WINDSURF - Making a FLASK APP EASY!!! - Resume Endpoint Setup (VIDEO 15)',
                'description': '''In this video, I set up the resume endpoint and make sure it's working correctly. I also go over how to handle errors and exceptions in the code, making sure the app remains stable even when things don't go as planned.'''
            },
            {
                'url': 'https://youtu.be/3zQvQ7ZzQ8k',
                'title': 'WINDSURF - Making a FLASK APP EASY!!! - Resume Endpoint Setup (VIDEO 16)',
                'description': '''In this video, I set up the resume endpoint and make sure it's working correctly. I also go over how to handle errors and exceptions in the code, making sure the app remains stable even when things don't go as planned.'''
            },
            {
                'url': 'https://youtu.be/3zQvQ7ZzQ8k',
                'title': 'WINDSURF - Making a FLASK APP EASY!!! - Resume Endpoint Setup (VIDEO 17)',
                'description': '''In this video, I set up the resume endpoint and make sure it's working correctly. I also go over how to handle errors and exceptions in the code, making sure the app remains stable even when things don't go as planned.'''
            },
            {
                'url': 'https://youtu.be/3zQvQ7ZzQ8k',
                'title': 'WINDSURF - Making a FLASK APP EASY!!! - Resume Endpoint Setup (VIDEO 18)',
                'description': '''In this video, I set up the resume endpoint and make sure it's working correctly. I also go over how to handle errors and exceptions in the code, making sure the app remains stable even when things don't go as planned.'''
            },
            {
                'url': 'https://youtu.be/3zQvQ7ZzQ8k',
                'title': 'WINDSURF - Making a FLASK APP EASY!!! - Resume Endpoint Setup (VIDEO 19)',
                'description': '''In this video, I set up the resume endpoint and make sure it's working correctly. I also go over how to handle errors and exceptions in the code, making sure the app remains stable even when things don't go as planned.'''
            }
        ]

        # Enhance video data with YouTube information
        videos = []
        for video_data in videos_data:
            try:
                video_id = extract_video_id(video_data['url'])
                logger.debug(f"Processing video ID: {video_id}")
                
                # Get the best available thumbnail
                thumbnail_url = get_best_thumbnail(video_id)
                logger.debug(f"Using thumbnail URL: {thumbnail_url}")
                
                # Start with our reliable hardcoded data
                video_info = {
                    'video_id': video_id,
                    'title': video_data['title'],
                    'description': video_data['description'],
                    'thumbnail_url': thumbnail_url
                }
                
                # Try to enhance with YouTube data, but don't let failures affect our basic functionality
                try:
                    yt = YouTube(f"https://youtube.com/watch?v={video_id}")
                    # Only update fields if we successfully get them
                    if hasattr(yt, 'views') and yt.views is not None:
                        video_info['view_count'] = yt.views
                    if hasattr(yt, 'publish_date') and yt.publish_date is not None:
                        video_info['publish_date'] = yt.publish_date.isoformat()
                    if hasattr(yt, 'length') and yt.length is not None:
                        video_info['length'] = yt.length
                    if hasattr(yt, 'author') and yt.author is not None:
                        video_info['author'] = yt.author
                    logger.debug(f"Successfully fetched additional YouTube data for {video_id}")
                except Exception as e:
                    logger.debug(f"Could not fetch additional YouTube data for {video_id}: {str(e)}")
                    # Continue with basic info only
                
                videos.append(video_info)
                logger.debug(f"Successfully processed video: {video_id}")
                
            except Exception as e:
                logger.error(f"Error processing video {video_data['url']}: {str(e)}")
                # Fallback to basic info
                videos.append({
                    'video_id': video_id,
                    'title': video_data['title'],
                    'description': video_data['description'],
                    'thumbnail_url': f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                })

        return jsonify(videos)
    except Exception as e:
        logger.error(f"General error in get_videos: {str(e)}")
        return jsonify({'error': str(e)}), 500
