from fastapi import FastAPI, Request, Form, Cookie, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional
from datetime import timedelta

import database
import auth

# Initialize FastAPI app
app = FastAPI(title="Database Viewer", version="1.0.0")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and create default admin user"""
    database.init_db()
    
    # Create default admin user if doesn't exist
    admin = database.get_admin_by_username("admin")
    if not admin:
        password_hash = auth.get_password_hash("admin123")
        database.create_admin("admin", password_hash)
        print("Default admin user created: admin/admin123")

def get_current_user(access_token: Optional[str] = Cookie(None)) -> Optional[dict]:
    """Get current user from access token cookie"""
    if not access_token:
        return None
    payload = auth.decode_access_token(access_token)
    if not payload:
        return None
    return payload

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, access_token: Optional[str] = Cookie(None), 
                message: Optional[str] = None, message_type: Optional[str] = None):
    """Home page - display all data entries"""
    user = get_current_user(access_token)
    data_entries = database.get_all_data()
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "data": data_entries,
        "is_admin": user is not None,
        "username": user.get("username") if user else None,
        "message": message,
        "message_type": message_type
    })

@app.get("/admin/login", response_class=HTMLResponse)
async def login_page(request: Request, access_token: Optional[str] = Cookie(None)):
    """Admin login page"""
    # If already logged in, redirect to home
    user = get_current_user(access_token)
    if user:
        return RedirectResponse(url="/", status_code=303)
    
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": None
    })

@app.post("/admin/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    """Handle admin login"""
    admin = database.get_admin_by_username(username)
    
    if not admin or not auth.verify_password(password, admin["password_hash"]):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid username or password"
        })
    
    # Create access token
    access_token = auth.create_access_token(
        data={"username": username},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    # Redirect to home with cookie
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return response

@app.post("/admin/logout")
async def logout():
    """Handle admin logout"""
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="access_token")
    return response

@app.get("/data")
async def get_data():
    """API endpoint to get all data entries"""
    data_entries = database.get_all_data()
    return {"data": data_entries}

@app.post("/data")
async def create_data(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    access_token: Optional[str] = Cookie(None)
):
    """Create a new data entry (admin only)"""
    user = get_current_user(access_token)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    database.create_data(title, description)
    return RedirectResponse(url="/?message=Entry created successfully&message_type=success", 
                          status_code=303)

@app.post("/data/{data_id}")
async def update_data(
    data_id: int,
    title: str = Form(...),
    description: str = Form(...),
    access_token: Optional[str] = Cookie(None)
):
    """Update a data entry (admin only)"""
    user = get_current_user(access_token)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    success = database.update_data(data_id, title, description)
    if not success:
        raise HTTPException(status_code=404, detail="Data entry not found")
    
    return RedirectResponse(url="/?message=Entry updated successfully&message_type=success",
                          status_code=303)

@app.delete("/data/{data_id}")
async def delete_data(data_id: int, access_token: Optional[str] = Cookie(None)):
    """Delete a data entry (admin only)"""
    user = get_current_user(access_token)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    success = database.delete_data(data_id)
    if not success:
        raise HTTPException(status_code=404, detail="Data entry not found")
    
    return JSONResponse(content={"message": "Entry deleted successfully"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
