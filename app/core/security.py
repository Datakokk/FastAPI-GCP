from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .firebase import verify_firebase_token, get_firebase_user
from typing import Dict, Optional, List, Any


security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from token"""
    token = credentials.credentials
    try:
        user_data = verify_firebase_token(token)
        
        custom_claims = user_data.get("custom_claims", {})

        result = {
            "uid": user_data.get("uid"),
            "email": user_data.get("email"),
            "email_verified": user_data.get("email_verified", False),
            "role": custom_claims.get("role", "user"),
            "permissions": custom_claims.get("permissions", [])
        }

        return result

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting current user: {str(e)}"
        )

class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, token_data: Dict[str, Any] = Depends(get_current_user)):
        user_role = token_data.get("role", "user")
        if user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {user_role} not permitted"
            )
        return token_data
        
# user checker
require_user = RoleChecker(["user", "admin"])

# admin checker
require_admin = RoleChecker(["admin"])

