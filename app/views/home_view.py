from fastapi import Request
from app.views import custom_render_templates


async def home_view(request: Request):
    return custom_render_templates(request, "index.html")
