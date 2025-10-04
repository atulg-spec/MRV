# apps/projects/urls.py
from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    # ---- Public / User-facing pages (templates) ----
    path("", views.ProjectListView.as_view(), name="project-list"),            # GET: list all public projects (dashboard view)
    path("mine/", views.MyProjectListView.as_view(), name="project-mine"),     # GET: list projects created by logged-in user/org
    path("create/", views.ProjectCreateView.as_view(), name="project-create"), # GET/POST: multi-step form (prototype wizard)

    # Optional: step-by-step wizard route (if using step param)
    path("create/step/<int:step>/", views.ProjectCreateStepView.as_view(), name="project-create-step"),

    path("<int:pk>/", views.ProjectDetailView.as_view(), name="project-detail"),      # GET: show full project + docs + photos
    path("<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="project-update"), # GET/POST: edit project (allowed while draft)
    path("<int:pk>/delete/", views.ProjectDeleteView.as_view(), name="project-delete"), # POST/DELETE

    # ---- Document & media handling (prototype: stored locally / simulated IPFS) ----
    path("<int:pk>/documents/", views.ProjectDocumentsView.as_view(), name="project-documents"),  # GET: list docs, POST: upload docs
    path("<int:pk>/documents/upload/", views.upload_project_document, name="project-document-upload"), # POST: single/multi file upload via AJAX
    path("<int:pk>/documents/<str:doc_id>/download/", views.download_project_document, name="project-document-download"), # GET: download file

    # ---- Workflow actions (submit / resubmit / request review) ----
    path("<int:pk>/submit/", views.submit_project_for_verification, name="project-submit"),   # POST: submit draft → becomes 'provisional'
    path("<int:pk>/resubmit/", views.resubmit_project, name="project-resubmit"),             # POST: submit corrected project after rejection
    path("<int:pk>/request-field-review/", views.request_field_review, name="project-request-field-review"), # POST

    # ---- Verification (NCCR / verifier UI) ----
    path("verify/queue/", views.VerificationQueueListView.as_view(), name="verification-queue"), # GET: list provisional records
    path("verify/<int:pk>/", views.verify_project_view, name="project-verify"),   # POST: approve (change status to 'approved')
    path("reject/<int:pk>/", views.reject_project_view, name="project-reject"),   # POST: reject with reason

    # ---- Audit / Actions history ----
    path("<int:pk>/history/", views.ProjectHistoryView.as_view(), name="project-history"), # GET: action log for audit trail

    # ---- Export / Reports ----
    path("<int:pk>/export/json/", views.export_project_json, name="project-export-json"), # GET: download project as JSON
    path("<int:pk>/export/pdf/", views.export_project_pdf, name="project-export-pdf"),   # GET: printable verification report (simulate)
    path("export/all/csv/", views.export_all_projects_csv, name="projects-export-csv"),   # GET: admin CSV export

    # ---- Misc / Admin helpers (prototype-level) ----
    path("mock/generate-cid/<int:pk>/", views.mock_generate_cid, name="project-mock-generate-cid"),     # POST: simulate IPFS CID generation (prototype)
    path("mock/generate-tx/<int:pk>/", views.mock_generate_txhash, name="project-mock-generate-tx"),    # POST: simulate txHash (optional demo)
]
