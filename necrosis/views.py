from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import ImageForm, LoginForm
from .models import Image
from .cbsdanalyzer import *
import json
import os
import csv
import zipfile
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Create your views here.
def index(request):
    return render(request, 'necrosis/cbsdscore.html', {})


def cbsdscore(request):
    return render(request, 'necrosis/cbsdscore.html', {})


# Image upload def
def uploadimage(request):
    if request.method == 'POST':
        initialPreview = []
        initialPreviewConfig = []
        form = ImageForm(request.POST, request.FILES)
        for f in request.FILES.getlist('images'):
            instance = Image(images=f)
            instance.save()

            img = resize_images(instance.images.url)
            img1, img1_name, img_cbsd_score = analyze_image(img)

            fpath = os.path.join('media/uploads/results', os.path.split(img1_name)[1])

            # writetocsv(
            #     request.user.get_username(),
            #     os.path.split(img1_name)[1], 
            #     img_cbsd_score,
            #     datetime.datetime.utcnow()
            #            )
            # pic = open(os.path.join(BASE_DIR, fpath), "r")
            # writetozippedfolder(request.user.get_username(), os.path.join(BASE_DIR, fpath))

            imgpath = "<img src='/"+fpath+"' style='height:260px' class='kv-preview-data krajee-init-preview file-preview-image' alt='RootResult' title='Root Result'>"
            imgconfig = {"type": "image", "caption": "CBSD Score:"+str(img_cbsd_score)+" %", "size": "847000"}

            initialPreview.append(imgpath)
            initialPreviewConfig.append(imgconfig)


        resu = {'initialPreview': initialPreview, 'initialPreviewAsData': 'false', 'initialPreviewConfig': initialPreviewConfig}
        return HttpResponse(json.dumps(resu))
        # return render(request, 'ppd/uploaded.html', {"sample": instance})

    else:
        form = ImageForm()
    return render(request, 'necrosis/cbsdscore.html', {})


# User logout def
# def userlogout(request):
#     if request.user.is_authenticated():
#         try:
#             os.remove(os.path.join(BASE_DIR, "media/uploads/results/"+request.user.get_username()+"_results.zip"))
#             logout(request)
#         except OSError:
#             pass
#         return redirect('necrosis:index')


# Create csv file
def createcsv(user):
        path = os.path.join(BASE_DIR, "media/uploads/csv/")
        if not os.path.exists(path):
            os.makedirs(path)
            c = csv.writer(open(os.path.join(BASE_DIR, "media/uploads/csv/" + user + "_results.csv"), "a"))
            c.writerow(["IMAGE NAME", "CBSD_SCORE (%)", "Date"])
        else:
            c = csv.writer(open(os.path.join(BASE_DIR, "media/uploads/csv/" + user + "_results.csv"), "a"))
            c.writerow(["IMAGE NAME", "CBSD_SCORE (%)", "Date"])


# Process CSV def
def writetocsv(user, imagename, cbsd_area, date):
    c = csv.writer(open(os.path.join(BASE_DIR, "media/uploads/csv/" + user + "_results.csv"), "a"))
    c.writerow([imagename, cbsd_area, date])


# Download csv def
def downloadcsv(request):
    if request.user.is_authenticated:
        user = request.user.get_username()
        path = os.path.join(BASE_DIR, "media/uploads/csv/" + user + "_results.csv")
        my_file = open(path, "r")
        response = HttpResponse(my_file, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=' + user + '_cbsd_results.csv'
        return response
    else:
        return redirect('necrosis:index')


# Download Zipped Folder def
def downloadzippedfolder(request):
    if request.user.is_authenticated:
        user = request.user.get_username()
        path = os.path.join(BASE_DIR, "media/uploads/results/" + user + "_results.zip")
        my_file = open(path, "rb")
        response = HttpResponse(my_file, content_type='application/x-zip-compressed')
        response['Content-Disposition'] = 'attachment; filename=' + user + '_cbsd image_results.zip'
        return response
    else:
        return redirect('necrosis:index')


# Create zipfile
def createzipfile(user):
    z = zipfile.ZipFile(os.path.join(BASE_DIR, "media/uploads/results/"+user+"_results.zip"), "w")
    z.close()


# Write to zipped folder
def writetozippedfolder(user, path):
    z = zipfile.ZipFile(os.path.join(BASE_DIR, "media/uploads/results/" + user + "_results.zip"), "a")
    z.write(path)
    z.close()
