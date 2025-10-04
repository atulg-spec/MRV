# apps/projects/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages

from .models import Project, ProjectDocument, ActionLog
from .forms import ProjectForm, DocumentUploadForm

# ------------------ Public / User-facing ------------------

class ProjectListView(ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.filter(status="approved")


class MyProjectListView(ListView):
    model = Project
    template_name = "projects/my_project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user)


class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/project_detail.html"
    context_object_name = "project"

class ProjectCreateStepView(View):
    """Prototype: Multi-step project creation (not fully implemented)."""
    template_name = "projects/project_form.html"

    def get(self, request, step=1):
        return render(request, self.template_name, {"step": step})


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("projects:project-mine")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Project created successfully (Draft).")
        return super().form_valid(form)


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("projects:project-mine")


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = "projects/project_confirm_delete.html"
    success_url = reverse_lazy("projects:project-mine")


# ------------------ Document Handling ------------------

class ProjectDocumentsView(View):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        docs = ProjectDocument.objects.filter(project=project)
        return render(request, "projects/project_documents.html", {"project": project, "documents": docs})

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.project = project
            doc.save()
            messages.success(request, "Document uploaded.")
        return redirect("projects:project-documents", pk=pk)


def upload_project_document(request, pk):
    # For AJAX upload (optional prototype)
    return JsonResponse({"status": "ok"})


def download_project_document(request, pk, doc_id):
    # Just a stub
    return HttpResponse(f"Download doc {doc_id} for project {pk}")


# ------------------ Workflow Actions ------------------

def submit_project_for_verification(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.status = "provisional"
    project.save()
    ActionLog.objects.create(project=project, action="submit", actor=request.user)
    messages.success(request, "Project submitted for verification.")
    return redirect("projects:project-detail", pk=pk)


def resubmit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.status = "provisional"
    project.save()
    ActionLog.objects.create(project=project, action="resubmit", actor=request.user)
    messages.success(request, "Project resubmitted.")
    return redirect("projects:project-detail", pk=pk)


def request_field_review(request, pk):
    project = get_object_or_404(Project, pk=pk)
    ActionLog.objects.create(project=project, action="field_review_requested", actor=request.user)
    messages.info(request, "Field review requested.")
    return redirect("projects:project-detail", pk=pk)


# ------------------ Verification ------------------

class VerificationQueueListView(ListView):
    model = Project
    template_name = "projects/verification_queue.html"
    context_object_name = "queue"

    def get_queryset(self):
        return Project.objects.filter(status="provisional")


def verify_project_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.status = "approved"
    project.save()
    ActionLog.objects.create(project=project, action="approved", actor=request.user)
    messages.success(request, "Project approved.")
    return redirect("projects:verification-queue")


def reject_project_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.status = "rejected"
    project.save()
    ActionLog.objects.create(project=project, action="rejected", actor=request.user)
    messages.error(request, "Project rejected.")
    return redirect("projects:verification-queue")


# ------------------ History / Audit ------------------

class ProjectHistoryView(DetailView):
    model = Project
    template_name = "projects/project_history.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["logs"] = ActionLog.objects.filter(project=self.object).order_by("-timestamp")
        return context


# ------------------ Export ------------------

def export_project_json(request, pk):
    return JsonResponse({"project": pk, "status": "demo"})


def export_project_pdf(request, pk):
    return HttpResponse("PDF export (prototype)")


def export_all_projects_csv(request):
    return HttpResponse("CSV export (prototype)")


# ------------------ Mock Blockchain Simulation ------------------

def mock_generate_cid(request, pk):
    return JsonResponse({"cid": f"fakeCID-{pk}"})


def mock_generate_txhash(request, pk):
    return JsonResponse({"txHash": f"fakeTx-{pk}"})
