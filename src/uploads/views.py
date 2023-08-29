from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home_view(request: HttpRequest):
    if request.method == "GET":
        user = request.user
        table_headers = ["Имя файла", "Состояние", "Отчёт по проверке"]
        items = Upload.objects.all()
        return render(request, "index.html", {"user": user,
                                              "items": items,
                                              "headers": table_headers,
                                              "message": "Файлов пока нет"})
