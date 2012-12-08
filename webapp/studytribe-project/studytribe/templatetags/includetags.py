from django import template

register = template.Library()

@register.inclusion_tag('inclusion_tags/include_js.html')
def include_js(jsname):
    return {'jsname':jsname}

@register.simple_tag
def current_time(format_string):
    return 'helloworld %s' % format_string
