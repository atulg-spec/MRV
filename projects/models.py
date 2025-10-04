# apps/projects/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Project(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("provisional", "Provisional (Submitted)"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    SPECIES_CHOICES = [
        ("Avicennia", "Avicennia (Factor: 2.5)"),
        ("Rhizophora", "Rhizophora (Factor: 3.0)"),
        ("Sonneratia", "Sonneratia (Factor: 2.0)"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    organization_name = models.CharField(max_length=255, blank=True, null=True)

    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    species = models.CharField(max_length=50, choices=SPECIES_CHOICES)
    seedling_count = models.PositiveIntegerField(default=0)

    notes = models.TextField(blank=True, default="")

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="projects")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class ProjectDocument(models.Model):
    DOC_TYPES = [
        ("land_paper", "Land Papers"),
        ("ngo_paper", "NGO Certification"),
        ("ngo_experience", "NGO Past Experience"),
        ("other", "Other"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="documents")
    doc_type = models.CharField(max_length=50, choices=DOC_TYPES)
    file = models.FileField(upload_to="project_docs/")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.title} - {self.get_doc_type_display()}"


class ActionLog(models.Model):
    ACTION_TYPES = [
        ("submit", "Submitted for Verification"),
        ("resubmit", "Resubmitted after Rejection"),
        ("approve", "Approved by Verifier"),
        ("reject", "Rejected by Verifier"),
        ("upload_doc", "Document Uploaded"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="actions")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    notes = models.TextField(blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.title} - {self.get_action_type_display()} ({self.timestamp:%Y-%m-%d})"
