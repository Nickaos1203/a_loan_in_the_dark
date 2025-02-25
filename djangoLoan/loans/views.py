from django.views.generic import CreateView, TemplateView, DetailView
from loans.models import Loan
from loans.forms import LoanForm
import requests
import os
from django.conf import settings
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from accounts.models import CustomUser
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils
import json
import pandas as pd

class LoanCreateView(CreateView):
    model = Loan
    template_name = "loans/create_loan.html"
    form_class = LoanForm
    success_url = reverse_lazy("loans:user_loan")

    def form_valid(self, form):
        """
        Méthode appelée si le formulaire est valide.
        1. Envoie les données du formulaire à l'API externe.
        2. Si succès, enregistre l'objet Loan en base de données.
        """
        user_info = self.request.session.get('user_info')
        user = get_object_or_404(CustomUser, id=user_info['id'])
        token = user.api_token
        headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json"
            }
        api_url = os.getenv("API_BASE_URL", settings.API_BASE_URL) + "/loans/create_loan"
        django_data = form.cleaned_data
        django_data["user_email"] = user.email

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

class LoanUserView(TemplateView):
    template_name = "loans/user_loan.html"

class AdvisorLoanDetailView(DetailView):
    model = Loan
    template_name = 'loans/advisor_loan.html'
    context_object_name = 'loan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loan = self.get_object()

        shap_values = loan.shap_values
        if not isinstance(shap_values, list) or not all(isinstance(x, (float, int)) for x in shap_values):
            shap_values = [float(x) for x in shap_values]
        print(shap_values)
        
        # Labels des caractéristiques dans le même ordre que les SHAP values
        features = ["State", "Bank", "NAICS", "Term", "NoEmp", "NewExist", "CreateJob", "RetainedJob", 
                    "UrbanRural", "RevLineCr", "LowDoc", "GrAppv", "Recession", "HasFranchise"]

        shap_df = pd.DataFrame({"Feature": features, "SHAP Value": shap_values})
        print(f"shap_df : {shap_df}")
        print(f"shap_df dtypes: {shap_df.dtypes}")

        # # Création du graphique avec les bonnes valeurs
        # fig = px.bar(
        #     shap_df, 
        #     x="SHAP Value", 
        #     y="Feature", 
        #     orientation="h", 
        #     title="Impact des caractéristiques sur la prédiction",
        #     color="SHAP Value", 
        #     color_continuous_scale="RdYlGn",
        #     category_orders={"Feature": shap_df["Feature"].tolist()} 
        # )


        # Création du graphique avec Plotly Graph Objects
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=shap_df["SHAP Value"],  
            y=shap_df["Feature"],  
            orientation="h",  
            marker=dict(color=shap_df["SHAP Value"], colorscale="RdYlGn"),
        ))

        # Mise en forme
        fig.update_layout(
            title="Impact des caractéristiques sur la prédiction",
            xaxis_title="SHAP Value",
            yaxis_title="Feature",
            yaxis=dict(categoryorder="total ascending"),  # Pour bien ordonner les features
        )

        # Convertir en JSON pour Django
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        # Ajouter au contexte Django
        context["graph_json"] = graph_json
        
        return context

