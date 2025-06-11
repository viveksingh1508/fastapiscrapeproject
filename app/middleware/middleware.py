from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.services.auth import get_current_user_from_cookie
from shared.backenddb import AsyncSessionLocal


class GetUserMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user = None
        async with AsyncSessionLocal() as db:
            try:
                user = await get_current_user_from_cookie(request, db)
            except Exception as e:
                print(f"middleware Exception {e}")
                user = None

            request.state.user = user

            response = await call_next(request)
        return response
