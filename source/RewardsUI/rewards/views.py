import logging
import requests

from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from .forms import OrderForm

class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__)):
        self.logger = logger

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        # Display form
        context["order_form"] = OrderForm()

        rewards_response = requests.get("http://rewardsservice:7050/rewards")
        context['rewards_data'] = rewards_response.json()

        all_customers_response = requests.get("http://rewardsservice:7050/customer/get_all")
        context['customer_data'] = all_customers_response.json()

        return TemplateResponse(
            request,
            self.template_name,
            context
        )


    def post(self, request, *args, **kwargs):
        print('request=%r' % request)
        if request.method == 'POST':
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                response = requests.post("http://rewardsservice:7050/customer/set_rewards", 
                              data = { "email" : order_form.cleaned_data['email'], 
                                       "order_total" : order_form.cleaned_data['order_total'] 
                                     })
                print('response=%r' % response.text)

                return HttpResponseRedirect('/rewards')