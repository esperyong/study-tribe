from django import template

register = template.Library()

def include_js(context,jsname,path='assets/studytribe/js/'):
    return {'jsname':jsname,
            'STATIC_URL':context['STATIC_URL'],
            'debug':context['debug'],
            'path':path}

register.inclusion_tag('inclusion_tags/include_js.html', 
                       takes_context=True)(include_js)


