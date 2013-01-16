# Create your views here.

def accept_invitation(request,invitation_key=None):
    context = {}
    return render_to_response("studytribe/studygroup/base.html",
                              context,
                              context_instance=RequestContext(request))

