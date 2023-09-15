from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from django.db.models import ObjectDoesNotExist
from django.core.exceptions import SuspiciousFileOperation
from users.models import CustomUser
from .models import Upload
from .forms import UploadForm, UploadDetailForm
# Create your views here.

@login_required
def home_view(request: HttpRequest):
    if request.method == "GET":
        user = request.user
        table_headers = ["Имя файла", "Состояние", "Отчёт по проверке"]
        user_instance = CustomUser.objects.get_by_natural_key(user)
        items = Upload.objects.filter(author=user_instance)
        return render(request, "index.html", {"user": user,
                                              "items": items,
                                              "headers": table_headers,
                                              "message": "Файлов пока нет"})

@login_required
def upload_file_view(request: HttpRequest):
    if request.method == "GET":
        return render(request, "upload.html", {"form": UploadForm,
                                               "user": request.user})
    elif request.method == "POST":
        form = UploadForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            upload_data = {"author": request.user,
                           "file": form.cleaned_data["file"]}
            upload = Upload.objects.create(**upload_data)
            upload.save()
            return redirect(reverse(home_view))
        else:
            return render(request, "upload.html", {"form": form,
                                                   "user": request.user,
                                                   "errors": form.errors})

@login_required
def upload_detail_view(request: HttpRequest, user:str, file:str):
    if str(request.user) != user and request.method:
        return HttpResponseForbidden()

    if request.method == "GET":
        try:
            file_instance = Upload.objects.filter(file=("submissions" + "/" + user + "/" + file)) 
        except ObjectDoesNotExist: 
            return HttpResponseNotFound
        except SuspiciousFileOperation:
            return HttpResponseBadRequest
        file = file_instance[0]
        with open(str(file.file), "r") as f:
            file_content = f.read()
        
        

        
        form = UploadDetailForm(initial={"author": file.author, "state": file.state, "file_content": file_content})
        return render(request, "upload_detail.html", {"user": request.user,
                                                      "form": form})

