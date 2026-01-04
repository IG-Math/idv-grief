# Database Viewer with FastAPI

A simple and elegant database viewer application built with Python and FastAPI. This application allows you to view data entries, log in as an admin, and manage data (create, update, delete) with admin privileges.

## Features

- 📊 **View Data**: Browse all data entries in an intuitive interface
- 🔐 **Admin Login**: Secure authentication for administrators
- ✏️ **Manage Data**: Create, update, and delete entries (admin only)
- 🎨 **Modern UI**: Beautiful, responsive design with gradient backgrounds
- 🔒 **JWT Authentication**: Secure session management with HTTP-only cookies
- 💾 **SQLite Database**: Lightweight database with no external dependencies

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

3. To access admin features, click "Admin Login" and use the default credentials:
   - **Username**: `admin`
   - **Password**: `admin123`

## API Endpoints

### Public Endpoints
- `GET /` - Home page with data viewer
- `GET /admin/login` - Admin login page
- `GET /data` - Get all data entries (JSON API)

### Admin-Only Endpoints
- `POST /admin/login` - Authenticate admin user
- `POST /admin/logout` - Logout admin user
- `POST /data` - Create a new data entry
- `POST /data/{id}` - Update an existing data entry
- `DELETE /data/{id}` - Delete a data entry

## Project Structure

```
idv-grief/
├── main.py              # FastAPI application
├── database.py          # Database operations
├── auth.py              # Authentication utilities
├── requirements.txt     # Python dependencies
├── templates/
│   ├── index.html      # Home page template
│   └── login.html      # Login page template
└── data.db             # SQLite database (created on first run)
```

## Security Notes

⚠️ **Important**: This is a demonstration application. For production use:
- Change the `SECRET_KEY` in `auth.py`
- Use environment variables for sensitive configuration
- Change the default admin password
- Use HTTPS in production
- Implement rate limiting for login attempts
- Add CSRF protection

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLite**: Lightweight database
- **Jinja2**: Template engine for HTML rendering
- **JWT**: Secure authentication tokens
- **Bcrypt**: Password hashing
- **Uvicorn**: ASGI server

## License

This project is open source and available for educational purposes.