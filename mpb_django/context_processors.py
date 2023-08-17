from config.models import NavigationLink
from mpb_django.enums import time_frames


def load_base_variables(request):
    print('called context proccessors')
    return {
        "timeframes": time_frames,
        'navigation_links': NavigationLink.objects.all().order_by("name")
    }