from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from .models import Job, JobApplication, APPLIED


class HomePageView(ListView):
    template_name = "main/home.html"
    queryset = Job.objects.all().order_by("-created_at")
    paginate_by = 6


class JobDetailView(DetailView):
    template_name = "main/job_detail.html"
    queryset = Job.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()
        if self.request.user.is_authenticated:
            application = JobApplication.objects.filter(user=self.request.user, job=job)
            context["has_applied"] = application.exists()
        return context


class ApplyJobView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_verified:
            messages.error(self.request, "Please verify your email first !")
            return redirect("home_page")
        try:
            if not self.request.user.userprofile.resume:
                messages.error(self.request, "Please upload your resume !")
                return redirect("home_page")
        except:
            messages.error(self.request, "Please complete your profile first !")
            return redirect("home_page")
        job_id = kwargs["job_id"]
        job = Job.objects.get(id=job_id)
        JobApplication.objects.create(job=job, user=self.request.user, status=APPLIED)
        messages.success(self.request, "Successfully applied to the Job !")
        return redirect("home_page")


class MyJobs(ListView):
    template_name = "main/my_jobs.html"

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)