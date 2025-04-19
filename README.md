# Master Blog

A simple Flask-based blog application that stores posts in a JSON file and supports full CRUD (Create, Read, Update, Delete) operations.

---

## Features

- **Add posts**: Users can create new blog posts via a form.
- **View posts**: Lists all posts on the home page with title, author, content, and timestamp.
- **Update posts**: Edit existing posts through a pre-populated form.
- **Delete posts**: Remove posts with a single click.
- **JSON storage**: All posts are saved in a `posts.json` file—no database required.

---

## Prerequisites

- Python 3.8+
- pip (Python package installer)

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/flask-json-blog.git
   cd flask-json-blog
   ```
2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. **Start the Flask app**
   ```bash
   python app.py
   ```
2. **Open your browser** and navigate to `http://localhost:5001/`
3. **Add, update, or delete** posts using the UI.

---

## Project Structure

```
masterblog/
├── app.py          
├── posts.json      
├── templates/      
│   ├── base.html
│   ├── index.html
│   ├── add.html
│   └── update.html
├── static/        
├── README.md     
└── requirements.txt
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m "Add YourFeature"`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---


## Acknowledgments

- [Flask Documentation](https://flask.palletsprojects.com/)
- Bootstrap for styling

