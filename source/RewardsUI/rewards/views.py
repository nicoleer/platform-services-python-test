import logging
import requests

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__)):
        self.logger = logger

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_response = requests.get("http://rewardsservice:7050/rewards")
        context['rewards_data'] = rewards_response.json()

        all_customers_response = requests.get("http://rewardsservice:7050/customer/get_all")
        context['customer_data'] = all_customers_response.json()

        return TemplateResponse(
            request,
            self.template_name,
            context
        )