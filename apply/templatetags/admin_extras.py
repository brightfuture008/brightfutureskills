from django import template

register = template.Library()

@register.simple_tag
def admin_page_url(cl, page_num):
    """
    Generates the URL for a specific page number in the admin changelist.
    page_num is 1-based (as displayed), but Django's 'p' parameter is 0-based.
    """
    if page_num == '.':
        return '#'
    try:
        page_index = int(page_num) - 1
    except (ValueError, TypeError):
        return '#'
    
    return cl.get_query_string({'p': page_index})