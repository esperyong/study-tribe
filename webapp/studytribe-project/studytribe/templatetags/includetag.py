from django import template

register = template.Library()

@register.inclusion_tag('inclusion_tags/include_js.html')
def includejs(jsname):
    return {'jsname':jsname}
