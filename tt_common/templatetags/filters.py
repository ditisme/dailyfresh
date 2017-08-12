from django.template import Library

register = Library()

@register.filter
def page_list(page):
    paginator = page.paginator
    page_range = paginator.page_range

    if paginator.num_pages > 5:
        if page.number < 3:
            page_range = range(1, 6)
        elif page.number > paginator.num_pages - 2:
            page_range = range(paginator.num_pages - 4, paginator.num_pages + 1)
        else:
            page_range = range(page.number - 2, page.number + 3)
    return page_range