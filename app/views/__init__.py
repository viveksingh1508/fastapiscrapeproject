from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")


def custom_render_templates(request, template_name, context={}):
    context["request"] = request
    context["user"] = getattr(request.state, "user", None)
    return templates.TemplateResponse(template_name, context)
