from fastapi import FastAPI, HTTPException, Depends, status
from firebase_admin import credentials, initialize_app, auth
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .core.security import get_current_user, require_user, require_admin
import uvicorn


app = FastAPI()




@app.get("/")
def health(user: dict = Depends(require_user)):
    return {
        "message": "This is a protected route",
        "uid": user["uid"],
        "email": user["email"],
        "role": user["role"],
        "permissions": user["permissions"]
    }

@app.get("/public")
def public():
    return {"message": "This is a public route"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
