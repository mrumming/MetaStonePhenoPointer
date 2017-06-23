from time import sleep
import json
from django.http import HttpResponse
from django.shortcuts import render

from MetaStone.models import AdminFileUpload


def main_view(request):
    return render(request, 'index.html')

def ajax_view(request):
    sleep(10) #This is whatever work you need
    pi1 = "This is pi1" #I just made pi1/pis1 random values
    pis1 = "This is pis1"
    context = {
        "pi1" : pi1,
        "pis1" : pis1,
    }
    data = json.dumps(context)

    return HttpResponse(data, content_type='application/json')

def process_uploads(request):
    uploads = AdminFileUpload.objects.filter(status="uploaded")
    for up_ in uploads:
        pass


def finished_uploads(request):

    uploads = AdminFileUpload.objects.filter(status="finished")

    if uploads:
        uploads = "<br/>".join([up_.__str__() for up_ in uploads])
    else:
        uploads = "None"

    return HttpResponse(uploads)
