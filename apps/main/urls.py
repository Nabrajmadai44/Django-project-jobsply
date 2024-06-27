from django.urls import path
from . import views


urlpatterns = [
    path("job/detail/<int:pk>/", views.JobDetailView.as_view(), name="job_detail"),
    path("apply-job/<int:job_id>/", views.ApplyJobView.as_view(), name="apply_job"),
    path("my-jobs/", views.MyJobs.as_view(), name="my_jobs"),
     path("khalti/", views.KhaltiPayment.as_view(), name="khalti_payment"),
    path("payment-verify/", views.PaymentVerify.as_view(), name="payment_verify"),
    path("", views.HomePageView.as_view(), name="home_page")
]