from rest_framework import renderers


class JSONRenderer(renderers.JSONRenderer):
    media_type = 'application/json'
    format = '.json'
    charset = None

    def render(self ,data , accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        
        if not str(status_code).startswith("2"):
            data = {'data': None , 'error' : data}
        else:
            data = {'data' : data , 'error' :None }
        return super(JSONRenderer, self).render(data, accepted_media_type, renderer_context)
