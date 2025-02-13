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
                'url': 'https://youtu.be/k8K3yxpaAfI',
                'title': 'WINDSURF 01 - Making a FLASK APP EASY!!! -  Initial Folder Structure and SETUP',
                'description': '''Introduction:
By the end of this video, you'll have a resume site that looks like this aaronjamespeters.onrender.com or you can change it, the code is also in my git, if youd like to just use that. This is a complete build, covering almost every step of problem-solving and debugging. Some of the more time-consuming debugging was shortened for the sake of the video, but I always explain how I fixed the issues. This is my first video series—there are more builds to come, and as I get better at making these, I hope you'll be able to build some awesome projects, too.

It's time we take back the tech industry and build entirely new AI driven OS systems/social sites from the ground up, not just patch the old ones. With AI tools like WINDSURF (and trust me, I've tried them all—WINDSURF is especially awesome!), we can create things that big companies—X, Insta, Apple, you name it—would love to stop, but we can steal users one by one. We have to start building before they notice, or they will stop us. Learning how to use AI coding tools like WINDSURF is crucial for the future.

This is about reclaiming tech, redistributing power, and showing how much better life can be without everything locked up in the hands of the 1%. There's an abundance of resources—we just don't distribute them fairly. The hoarders of wealth and power seem content to let the rest of us suffer under their greed. But really, how much does one person need to be truly happy? Isn't a good life about having great family and friends by your side?

I'm not here to show half the process and pretend it works—I'm giving you the full picture. This video starts with an explanation of the initial folder structure and how to set up a basic Python Flask app using WINDSURF, Cascade (the AI platform and my name for the AI Cassi), Codeium (the AI assistant), and WINDSURF (the code editor). This series of videos will walk you through building a work application demo page that I'm using to apply for jobs. Follow along, and I'll show you everything you need to know about setting up your own Python Flask app—from key considerations to all the essential steps.

In this first video, I go over the folder structure that I pre-made with OpenAI. For this simple app—or any app—it's really helpful to predesign the folders and basic scripts you'll need to render everything in the browser. Laying that foundation makes things much easier down the line. AI tools can generate scripts, but when those scripts are linked to others, there's always a chance it will accidentally break features you've already set up. While anything can be fixed if you ask the right questions (Best practices usually), you can easily get stuck in loops and waste tokens. For the planet's sake, it's best to avoid that whenever possible.

As I get better at this, I'll move on to more complex projects—some of which I've already built but plan to rebuild. I haven't been coding for long, but the learning curve I've experienced with AI code editing tools like WINDSURF has been unparalleled. I already have two projects in mind, both built with Django. Stay tuned!

My name is Aaron James Peters and thank you for watching.'''.strip(),
            },
            {
                'url': 'https://youtu.be/o9kdfk1Q-L0',
                'title': 'WINDSURF 02 - Making a FLASK APP EASY!!! - Finishing folder structure',
                'description': '''In this video, I demonstrate how WINDSURF editor and Codeium AI collaborate to generate a portion of the folder structure for a Flask app. Since Codeium can't generate the entire Flask application in one go, I walk you through what it successfully generated, how far it got, and how much more is required for the app to run locally in the browser. This highlights the gaps and the additional steps needed to complete the setup. I completely forget to run the commands and wonder why it's not running. NUBE Lol!'''
            },
            {
                'url': 'https://youtu.be/eFMfZ0CFbKM',
                'title': 'WINDSURF 03 - Making a FLASK APP EASY!!! - Setting up the .venv folder',
                'description': '''In this video, I set up the .venv folder and ensure all dependencies are installed. I run into a few issues that require troubleshooting before totally forgetting to run the commands for the app to start wondering what happened, definitely a nube just like in the last video. Lol In the next video we get it started, though. One key tip: when working in local development, avoid using HTTPS—it can clutter your terminal output and make it difficult to read.'''
            },
            {
                'url': 'https://youtu.be/eqmBMIs2y8E',
                'title': 'WINDSURF 04 - Making a FLASK APP EASY!!! - Troubleshooting/Debugging',
                'description': '''BY THE END I'M RUNNING IN LOCAL DEV. IT BEEN MAYBE 30-45 MIN TOPS. This would take a team a whole week. In this video, watch me coach Cody (Codeium AI) as it tries to render the initial setup of the Flask app. It’s a bit of a struggle, and I make a few simple mistakes along the way, but in the end, I get the app up and running. A reminder that coding is all about persistence and learning from those small errors!'''
            },
            {
                'url': 'https://youtu.be/gAnmIrpZmkA',
                'title': 'WINDSURF 05 - Making a FLASK APP EASY!!! - FORGOT!!! git init',
                'description': '''In this video, I initialize Git and start tracking the project folder—something I really should have done from the start! Luckily, with WINDSURF editor and Codeium AI, getting everything set up correctly was quick and easy. I also create a dev branch and begin working from there, following best practices for development.'''
            },
            {
                'url': 'https://youtu.be/3WHWDnJM6FI',
                'title': 'WINDSURF 06 - Making a FLASK APP EASY!!! - Different Logging Levels w/ quick chat',
                'description': '''In this video, I walk through setting up logging for both development and production using WINDSURF editor chat. The goal is to configure logging so development has detailed local debugging, while production only tracks error and info logs. This setup makes it much easier to debug locally and monitor server-side activity. It also helps identify any unusual behavior from users, keeping the app secure and running smoothly.'''
            },
            {
                'url': 'https://youtu.be/2aAKnZ_dET4',
                'title': 'WINDSURF 07 - Making a FLASK APP EASY!!! - DEBUG-.env creation & more DEBUGGING',
                'description': '''In this video, I run into some challenges setting up proper logging. I create the essential .env file, but I struggle to get the logging configuration to work seamlessly between the .env, base.py, and its dependent configuration files—dev.py for local development and prod.py for deployment. I also go over how I set up the .env file to manage the environment for each configuration, ensuring that dev.py is used for local development and prod.py is ready for deployment. It’s a great reminder that fine-tuning these configurations takes time but is crucial for a smooth development workflow.'''
            },
            {
                'url': 'https://youtu.be/BoZsNXwjxKo',
                'title': 'WINDSURF 08 - Making a FLASK APP EASY!!! - Explainer of off Camera Logging Setup',
                'description': '''In this video, I recap all the off-camera debugging and setup required to get the logging flow working properly. I couldn’t show every step, but the key challenge was configuring the .env file to work seamlessly with .env.development and .env.production. These files connect through base.py in the config folder to ensure the right logging settings are applied from dev.py for development and prod.py for production. Since .env.production needs a secure token (secrets.token_hex(32)), I created a .env.production.template file to show the structure without exposing sensitive info. When deploying to Render, I’ll generate the token and copy it into the actual .env.production file. DISCLAIMER: made this a little more complicated than it needs to be, best thing is to work in local development and you can check production is working with the variables in the .env file even though I separated the .env.production .env.developemnt, although you can just upload the .env production variables later. For something this simple it not required. You couuld just do a simple set up in the .env.'''
            },
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
