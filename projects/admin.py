# apps/projects/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Project, ProjectDocument, ActionLog


class ProjectDocumentInline(admin.TabularInline):
    model = ProjectDocument
    extra = 1
    fields = ("doc_type", "file", "uploaded_at")
    readonly_fields = ("uploaded_at",)


class ActionLogInline(admin.TabularInline):
    model = ActionLog
    extra = 0
    fields = ("action_type", "notes", "user", "timestamp")
    readonly_fields = ("timestamp",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "organization_name",
        "status_colored",
        "species",
        "seedling_count",
        "created_by",
        "created_at",
        "document_count",
    )
    list_filter = ("status", "species", "created_at")
    search_fields = ("title", "organization_name", "created_by__username")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [ProjectDocumentInline, ActionLogInline]

    fieldsets = (
        ("Project Info", {
            "fields": ("title", "description", "organization_name", "status")
        }),
        ("Location", {
            "fields": ("location", ("latitude", "longitude"))
        }),
        ("Plantation Details", {
            "fields": ("species", "seedling_count", "notes")
        }),
        ("Metadata", {
            "fields": ("created_by", "created_at", "updated_at")
        }),
    )

    def status_colored(self, obj):
        colors = {
            "draft": "gray",
            "provisional": "orange",
            "approved": "green",
            "rejected": "red",
        }
        color = colors.get(obj.status, "black")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display(),
        )
    status_colored.short_description = "Status"

    def document_count(self, obj):
        return obj.documents.count()
    document_count.short_description = "Documents"


@admin.register(ProjectDocument)
class ProjectDocumentAdmin(admin.ModelAdmin):
    list_display = ("project", "doc_type", "file", "uploaded_at")
    list_filter = ("doc_type", "uploaded_at")
    search_fields = ("project__title",)
    readonly_fields = ("uploaded_at",)


@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ("project", "action_type", "user", "timestamp", "short_notes")
    list_filter = ("action_type", "timestamp")
    search_fields = ("project__title", "user__username", "notes")
    readonly_fields = ("timestamp",)

    def short_notes(self, obj):
        return (obj.notes[:40] + "...") if len(obj.notes) > 40 else obj.notes
    short_notes.short_description = "Notes"
