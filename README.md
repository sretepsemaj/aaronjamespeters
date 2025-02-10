# Aaron James Peters Profile App

A modern Flask web application showcasing my professional profile, projects, and YouTube content.

## Features

- Bio page with professional background
- Interactive resume section
- GitHub projects showcase
- YouTube video gallery
- Responsive design for all devices
- Modern UI with smooth animations

## Technology Stack

- Flask 3.0.0
- Python 3.x
- Bootstrap 5
- Font Awesome
- AOS (Animate On Scroll)

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/sretepsemaj/aaronjamespeters.git
cd aaronjamespeters
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.development.template .env.development
# Edit .env.development with your settings
```

5. Run the development server:
```bash
python run.py
```

## Deployment

1. Set up production environment:
```bash
cp .env.production.template .env
# Edit .env with production settings
```

2. Required environment variables:
- `FLASK_ENV`: Set to 'production'
- `SECRET_KEY`: Your secret key
- `YOUTUBE_API_KEY`: Your YouTube API key

3. The app is configured to run with gunicorn in production:
```bash
gunicorn run:app
```

## Project Structure

- `/app`: Main application package
  - `/blueprints`: Route blueprints
  - `/media`: Media files (images and text content)
  - `/templates`: HTML templates
- `/config`: Configuration files
- `run.py`: Application entry point

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
