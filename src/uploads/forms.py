from django import forms
from .models import Upload

class UploadForm(forms.Form):
    file = forms.FileField(label="Файл на проверку",
                           required=True,
                           widget=forms.ClearableFileInput)
    def clean_file(self):
        file = self.cleaned_data.get("file")
        if file:
            if not file.name.endswith(".py"):
                raise forms.ValidationError("Only .py files are allowed")
            return file

class UploadDetailForm(forms.Form):
    author = forms.CharField(label="Автор", max_length=255, disabled=True)
    state = forms.CharField(label="Состояние", max_length=255, disabled=True)
    file_content = forms.FileField(label="Содержимое файла", widget=forms.Textarea, disabled=True)
    
