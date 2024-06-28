# import requests
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView, View, TemplateView
from django.contrib import messages
from django.db.models import OuterRef, Exists, Value
from django.urls import reverse_lazy
from .models import Job, JobApplication, APPLIED, Category


class HomePageView(ListView):
    template_name = "main/home.html"
    paginate_by = 6

    def get_queryset(self):
        try:
            applied_jobs = JobApplication.objects.filter(
                user=self.request.user,
                job=OuterRef('pk')
            )
            qs = Job.objects.all().annotate(applied=Exists(applied_jobs)).order_by("-created_at")
        except:
            qs = Job.objects.all().annotate(applied=Value(False)).order_by("-created_at")
        search = self.request.GET.get("search")
        if search:
            qs = qs.filter(title__icontains=search)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["categories"] = Category.objects.all()
        return context


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


class KhaltiPayment(TemplateView):
    template_name = "main/khalti_payment.html"

class PaymentVerify(View):
    def post(self, *args, **kwargs):
        verification_url = "https://khalti.com/api/v2/payment/verify/"
        print(self.request.POST)
        token = self.request.POST.get("token")
        amount = 1000
        data = dict(token=token, amount=amount)
        headers = {
            'Authorization': 'Key test_secret_key_7f05835f6e0c4511a35e2dd7eeacb82d'
        }
        # response = requests.post(verification_url, data=data, headers=headers)
        # if response.status_code in [200, "200"]:
            # print("Payment Success !!")
        #     messages.success(self.request, "Payment Success!!")
        #     return redirect("home_page")
        # messages.error(self.request, "Could not verify the payment")
        # return redirect("home_page")