from core.decorators import render_template

@render_template
def app(request):
    return "inc/app.html"
