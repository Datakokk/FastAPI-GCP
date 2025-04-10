"""Configuration for Firebase"""
from firebase_admin import credentials, initialize_app, auth
import firebase_admin
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .config import settings
from fastapi import HTTPException, status
import os
import json

def initialize_firebase():
    """Initialize Firebase"""
    try:
        if settings.FIREBASE_CREDENTIALS_PATH and os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            return firebase_admin.initialize_app(cred)
        elif settings.FIREBASE_CREDENTIALS_JSON:
            try:
                service_account = json.loads(settings.FIREBASE_CREDENTIALS_JSON)
                cred = credentials.Certificate(service_account)
                return firebase_admin.initialize_app(cred)
            except Exception as e:
                raise ValueError(f"Failed to parse Firebase credentials: {e}")
        else:
            return firebase_admin.initialize_app()
        
    except Exception as e:
        raise ValueError(f"Failed to initialize Firebase: {e}")

firebase_app = initialize_firebase()

def verify_firebase_token(token: str):
    if not firebase_app:
        raise HTTPException(status_code=500, detail="Firebase app not initialized")
    
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid" 
        )
    except auth.RevokedIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token revoked"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication error: {str(e)}"
        )
    

def get_firebase_user(uid: str):
    """Get user information from Firebase by UID."""
    if not firebase_app:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service not available"
        )
    
    try:
        return auth.get_user(uid)
    except auth.UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found: {uid}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting user: {str(e)}" 
        )