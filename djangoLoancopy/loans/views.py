from django.views.generic import CreateView
from loans.models import Loan
from loans.forms import LoanForm
import requests
import os
from django.conf import settings
from django.urls import reverse_lazy
from django.http import JsonResponse

class LoanCreateView(CreateView):
    model = Loan
    template_name = "loans/create_loan.html"
    form_class = LoanForm
    success_url = reverse_lazy("loan_success")

    def form_valid(self, form):
        """
        Méthode appelée si le formulaire est valide.
        1. Envoie les données du formulaire à l'API externe.
        2. Si succès, enregistre l'objet Loan en base de données.
        """
        user = self.request.user
        token = user.api_token
        headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json"
            }
        api_url = os.getenv("API_BASE_URL", settings.API_BASE_URL) + "/create_loan"
        django_data = form.cleaned_data

        try:
            response = requests.post(api_url, json=django_data, headers=headers)
            data = response.json()

            if response.status_code == 201:
                form.instance.id = data.get("id")
                form.instance.user = user
                form.instance.status = data.get("status")
                form.instance.prediction = data.get("prediction") 
                form.instance.proba_yes = data.get("proba_yes")
                form.instance.proba_no = data.get("proba_no")
                form.instance.shap_values = data.get("shap_values")
                form.instance.state = data.get("state")
                form.instance.bank = data.get("bank")
                form.instance.naics = data.get("naics")
                form.instance.rev_line_cr = data.get("rev_line_cr")
                form.instance.low_doc = data.get("low_doc")
                form.instance.new_exist = data.get("new_exist")
                form.instance.has_franchise = data.get("has_franchise")
                form.instance.recession = data.get("recession")
                form.instance.urban_rural = data.get("urban_rural")
                form.instance.create_job = data.get("create_job")
                form.instance.retained_job = data.get("retained_job")
                form.instance.no_emp = data.get("no_emp")
                form.instance.term = data.get("term")
                form.instance.gr_appv = data.get("gr_appv")

                return super().form_valid(form)
            else:
                return JsonResponse({"error": data}, status=response.status_code)

        except requests.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)

    def form_invalid(self, form):
        """
        Méthode appelée si le formulaire est invalide.
        """
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"errors": form.errors}, status=400)
        return super().form_invalid(form)
