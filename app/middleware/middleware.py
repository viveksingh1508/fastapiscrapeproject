from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.views.auth_view import get_user


class GetUserMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            user = await get_user(request)
        except Exception:
            user = None

        request.state.user = user

        response = await call_next(request)
        return response
