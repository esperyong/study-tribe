from django import template

register = template.Library()

def include_js(context,jsname,path='assets/studytribe/js/'):
    return {'jsname':jsname,
            'STATIC_URL':context['STATIC_URL'],
            'debug':('debug' in context),
            'path':path}

def include_css(context,cssname,path='assets/studytribe/css/'):
    return {'cssname':cssname,
            'STATIC_URL':context['STATIC_URL'],
            'debug':('debug' in context),
            'path':path}


register.inclusion_tag('inclusion_tags/include_js.html', 
                       takes_context=True)(include_js)

register.inclusion_tag('inclusion_tags/include_css.html', 
                       takes_context=True)(include_css)

