# from fastapi import Request, HTTPException, status, Depends
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.models.user import User
# from app.auth.jwt import create_access_token


# class JWTBearer(HTTPBearer):
#     def __init__(self, auto_error: bool = True):
#         super().__init__(auto_error=auto_error)

#     def __call__(self, request: Request, db: Session = Depends(get_db)):
#         credentials: HTTPAuthorizationCredentials = super().__call__(request)

#         # Validate scheme
#         if credentials.scheme != "Bearer":
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Invalid authentication scheme"
#             )

#         token = credentials.credentials
#         return self.verify_jwt(token, db)

#     def verify_jwt(self, token: str, db: Session):
#         try:
#             payload = create_access_token(token)
#             user_id = payload.get("sub")

#             if user_id is None:
#                 raise HTTPException(
#                     status_code=status.HTTP_401_UNAUTHORIZED,
#                     detail="Token payload missing user id"
#                 )

#             # Check user existence in DB
#             user = db.query(User).filter(User.id == user_id).first()

#             if not user:
#                 raise HTTPException(
#                     status_code=status.HTTP_401_UNAUTHORIZED,
#                     detail="User not found"
#                 )

#             return user  # return user to route

#         except Exception as e:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail=f"Invalid or expired token: {str(e)}"
#             )



from fastapi import Request, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.auth.jwt import verify_access_token
from datetime import datetime

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request, db: Session = Depends(get_db)):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or missing authorization token"
            )

        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication scheme"
            )

        # Validate token
        user = self.verify_jwt(credentials.credentials, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        return user  # <- IMPORTANT: return the user

    def verify_jwt(self, token: str, db: Session):
        try:
            payload = verify_access_token(token)
            user_id = payload.get("sub")

            if user_id is None:
                return None

            user = db.query(User).filter(User.id == user_id).first()
            return user

        except Exception:
            return None


authMiddleware = JWTBearer()
