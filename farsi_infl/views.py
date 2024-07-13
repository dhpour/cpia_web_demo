from django.shortcuts import render
from cpia import FarsiAnalyzer, Converter
# Create your views here.

from django.http import HttpResponse
from django.template import Context, loader
import re

farsi = FarsiAnalyzer()
converter = Converter(farsi)
numbers_pattern = "۱۲۳۴۵۶۷۸۹۰"

def index(request):
    template = loader.get_template("farsi_infl/index.html")
    return HttpResponse(template.render())
    
def getInflection(request):
    if request.method == 'GET':
        word = request.GET.get('word', None)
        fst = int(request.GET.get('fst', '1'))
        if word:
            inflection = []

            if fst ==1:
                inflection = [x for x in farsi.inflect(word)]
            elif fst == 6:
                inflection = [x for x in farsi.generate(word)]
            elif fst == 2:
                inflection = [x for x in converter.convert(word, "informal")]
            elif fst == 3:
                inflection = [x for x in converter.convert(word, "formal")]
        
            info = {}

            for l in inflection:
                for x in l.split('='):
                    for y in x.split("+"):
                        y = re.sub("[" + numbers_pattern + "]", "", y)
                        detail = farsi._parts_help.get(y, '')
                        if detail:
                            info[y] = detail

            out = '\nتوضیحات:\n'
            for abbr in list(info.keys()):
                out += "🔹  " + abbr + " 👈 " + info[abbr] + "\n"
            
            inflection = '\n'.join(["🔹  " + x for x in inflection])
            inflection = word + "\n\n" + inflection
            if fst == 1:
                inflection += "\n" + out

            return HttpResponse(inflection) # Sending an success response
        return HttpResponse("")

    return HttpResponse("Request method is not a GET")