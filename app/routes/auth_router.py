from fastapi import APIRouter, Depends, Request, HTTPException
from app.views import auth_view
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from shared.backenddb import get_db
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from fastapi import status
import uuid
from app.helper.redis import set_session_data, sign_session_id
from app.services.auth import oauth
from shared.models import User

router = APIRouter()


@router.get("/google/login")
async def login_wiht_google(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, session: AsyncSession = Depends(get_db)):
    try:
        # This call now correctly returns the 'token' dictionary, which
        # includes 'access_token', 'id_token', and the parsed 'userinfo'.
        token = await oauth.google.authorize_access_token(request)
        print("Full token received:", token)  # Keep for debugging

        # --- CORRECTED LINE: Access 'userinfo' directly from the 'token' dictionary ---
        user_info = token.get("userinfo")

        if not user_info:
            print("User info not found in token response after authorization.")
            return RedirectResponse(
                url="/auth/login?error=Authentication_failed",
                status_code=status.HTTP_302_FOUND,
            )

        # Extract relevant user info
        google_id = user_info.get(
            "sub"
        )  # 'sub' is the unique subject identifier from OIDC
        email = user_info.get("email")
        name = user_info.get("name", email)  # Use name if available, else email

        # Check if a user already exists.
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                email=email,
                username=email,
                first_name=name.split(" ")[0],
                last_name=(
                    " ".join(name.split(" ")[1:]) if len(name.split(" ")) > 1 else ""
                ),
                password=None,
                google_id=google_id,
            )

            try:
                session.add(user)
                await session.commit()
                await session.refresh(user)
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=400, detail="Registration failed due to database error"
                )

        else:
            if not user.google_id:
                user.google_id = google_id
                await session.commit()

        # Store session data in Redis (or your chosen session store)
        session_id = str(uuid.uuid4())
        session_data = {
            "user_id": user.id,
            "email": email,
            "name": f"{user.first_name} {user.last_name}",
        }
        await set_session_data(session_id, session_data)

        response = RedirectResponse(url="/")
        # Ensure sign_session_id matches how you setup your session handling
        response.set_cookie("session_id", sign_session_id(session_id), httponly=True)
        return response

    except Exception as e:
        print(f"Error during Google callback: {e}")
        import traceback

        traceback.print_exc()  # Print full traceback for detailed debugging
        return RedirectResponse(
            url="/auth/login?error=Google_authentication_failed",
            status_code=status.HTTP_302_FOUND,
        )


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, db: AsyncSession = Depends(get_db)):
    return await auth_view.login_view(request, db)


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, db: AsyncSession = Depends(get_db)):
    return await auth_view.login_view(request, db)


@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    return await auth_view.logout(request)
