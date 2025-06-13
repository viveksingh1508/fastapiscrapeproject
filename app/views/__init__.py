from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")


def custom_render_templates(request, template_name, context={}, status_code=200):
    context["request"] = request
    context["user"] = getattr(request.state, "user", None)
    return templates.TemplateResponse(template_name, context, status_code=status_code)
