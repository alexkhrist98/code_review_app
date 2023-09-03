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

class UploadDetailForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ["author", "file", "state"]
        labels = {
            "author": "Автора",
            "file": "Содержимое файла",
            "State": "Состояние"
        }

