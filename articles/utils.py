from datetime import date
def template_formatting(request, template_val):
    today = date.today()
    return template_val.replace('%year', today.strftime('%Y')) \
        .replace('%month',  today.strftime('%m')) \
        .replace('%day', today.strftime('%d')) \
        .replace('%name', request.user.username)
