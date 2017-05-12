from django.utils.deprecation import MiddlewareMixin
# new to django from 1.10 - subclass MiddlewareMixin
# http://stackoverflow.com/questions/39457381/object-takes-no-parameters-in-django-1-10


class HujMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'country' in request.session:
            return None
        else:
            if 'HTTP_ACCEPT_LANGUAGE' in request.META.keys():
                langs = self.parseAcceptLanguage(request.META['HTTP_ACCEPT_LANGUAGE'])
                if langs:
                    pair = langs[0][0]
                    c = pair.split('-')[1]
                    request.session['country'] = c
                    print(c)
        return None

    # https://siongui.github.io/2012/10/11/python-parse-accept-language-in-http-request-header/#id5
    # https://siongui.github.io/2012/10/12/detect-user-language-locale-gae-python/
    def parseAcceptLanguage(self, acceptLanguage):
        languages = acceptLanguage.split(",")
        locale_q_pairs = []
        for language in languages:
            if language.split(";")[0] == language:
                # no q => q = 1
                locale_q_pairs.append((language.strip(), "1"))
            else:
                locale = language.split(";")[0].strip()
                q = language.split(";")[1].split("=")[1]
                locale_q_pairs.append((locale, q))
        return locale_q_pairs