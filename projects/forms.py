# apps/projects/forms.py
from django import forms
from .models import Project, ProjectDocument


class ProjectForm(forms.ModelForm):
    """
    Form for creating/updating Project.
    Initially, keep it simple — core fields only.
    You can add validation rules later (e.g., land papers required).
    """
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "location",
            "latitude",
            "longitude",
            "species",
            "seedling_count",
            "notes",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter project name"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Brief project description"}),
            "location": forms.TextInput(attrs={"class": "form-control", "placeholder": "Village/Area/Region"}),
            "latitude": forms.NumberInput(attrs={"class": "form-control", "step": "0.000001"}),
            "longitude": forms.NumberInput(attrs={"class": "form-control", "step": "0.000001"}),
            "species": forms.Select(attrs={"class": "form-control"}),
            "seedling_count": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Any additional notes"}),
        }


class DocumentUploadForm(forms.ModelForm):
    """
    Handles file uploads (land papers, NGO certs, etc.).
    Prototype: accept any file. Later you can restrict extensions (PDF, JPG, PNG).
    """
    class Meta:
        model = ProjectDocument
        fields = ["doc_type", "file"]
        widgets = {
            "doc_type": forms.Select(attrs={"class": "form-control"}),
            "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
