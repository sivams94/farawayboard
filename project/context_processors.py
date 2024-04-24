from .utils import get_sidebar_menu

def menu_links(request):
  return {'menu_links': get_sidebar_menu()}