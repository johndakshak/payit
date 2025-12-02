from fastapi import APIRouter, HTTPException, status, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.enums import Gender
from app.schema.users_schema import UserCreate, UserResponse, UserUpdate
from app.security import hash_password
from app.middleware.auth import JWTBearer
from app.middleware.auth import authMiddleware
from app.config.oauth import oauth
from app.config.oauth import AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CALLBACK_URL, AUTH0_CLIENT_SECRET
from app.auth.jwt import create_access_token
from fastapi.responses import RedirectResponse
import pymysql

router = APIRouter(prefix="/oauth", tags=["Oauth"])

@router.get('/login')
async def login(request: Request):
    redirect_url = request.url_for("callback")
    try:
        return await oauth.auth0.authorize_redirect(request, redirect_uri=redirect_url)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Auth Error: Failed to authenticate User: {e}"
        )


@router.get('/callback', name='callback')
async def callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.auth0.authorize_access_token(request)
        print("User token", token)

        user_info = token.get("userinfo")

        user = db.query(User).filter(User.email == user_info["email"]).first()

        if not user:
            user = User(
                name=user_info.get("name"),
                phone="12345678901",
                email=user_info["email"],
                password=hash_password("James1"),
                gender=Gender.M.value,
                location="Jos"
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        jwt = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "user_id": str(user.id)
            }
        )

        return {
            "access_token": jwt,
            "email": user.email,
            "id": user.id
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Auth Error: Failed to generate token {e}"
        )

    except pymysql.DataError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"DB Error: {e}"
        )


@router.get('/logout')
def logout(request: Request):
    return_url = "http://localhost:8000"

    logout_url = (
        f"https://{AUTH0_DOMAIN}/v2/logout"
        f"?client_id={AUTH0_CLIENT_ID}"
        f"&returnTo={return_url}"
    )

    return RedirectResponse(url=logout_url)
