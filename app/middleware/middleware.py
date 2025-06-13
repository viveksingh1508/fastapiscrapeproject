from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.helper.redis import (
    get_session_data,
    set_session_data,
    sign_session_id,
    unsign_session_id,
    SESSION_COOKIE_NAME,
    SESSION_TTL,
)
import uuid
from shared.backenddb import AsyncSessionLocal
from app.views.auth_view import get_user_view


class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        session_id = None
        signed_session_id = request.cookies.get(SESSION_COOKIE_NAME)

        if signed_session_id:
            session_id = unsign_session_id(signed_session_id)

        request.state.session_id = session_id
        request.state.session = {}

        if session_id:
            data = await get_session_data(session_id)
            if data:
                request.state.session = data
        response: Request = await call_next(request)

        if request.state.session_id and request.state.session:
            await set_session_data(request.state.session_id, request.state.session)

        if not request.state.session_id and request.state.session:
            new_id = str(uuid.uuid4())
            signed_id = sign_session_id(new_id)
            await set_session_data(new_id, request.state.session)
            response.set_cookie(
                SESSION_COOKIE_NAME,
                signed_id,
                httponly=True,
                samesite="lax",
                max_age=SESSION_TTL,
            )

        return response


class LoadUserMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.user = None
        async with AsyncSessionLocal() as db:
            try:
                user = await get_user_view(request, db)
            except Exception as e:
                print(f"User middleware Exception {e}")
                user = None
            request.state.user = user
        response = await call_next(request)
        return response
