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


# oauth2_scheme = HTTPBearer()

# async def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
#     db: AsyncSession = Depends(get_db),
# ):
#     token = credentials.credentials
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         if payload.get("type") != "access":
#             raise HTTPException(status_code=401, detail="Invalid token type")

#         user = await get_user(payload["user_id"], db)
#         if not user or not user.is_active:
#             raise HTTPException(status_code=401, detail="User inactive")
#         return user
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")
