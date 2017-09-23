import logging
import requests

from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from .forms import OrderForm
from .forms import SearchForm

class RewardsView(TemplateView):
    template_name = 'index.html'
    rewards = requests.get("http://rewardsservice:7050/rewards").json()

    def __init__(self, logger=logging.getLogger(__name__)):
        self.logger = logger

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        # Display forms and rewards information
        context['order_form'] = OrderForm()
        context['search_form'] = SearchForm()
        context['rewards_data'] = self.rewards

        all_customers_response = requests.get("http://rewardsservice:7050/customer/get_all")
        context['customer_data'] = all_customers_response.json()
        context['show_reset_button'] = False

        return TemplateResponse(
            request,
            self.template_name,
            context
        )


    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if request.method == 'POST':
            order_form  = OrderForm(request.POST)
            search_form  = SearchForm(request.POST)

            # handle order form
            if 'order-button' in request.POST and order_form.is_valid():
                response = requests.post("http://rewardsservice:7050/customer/set_rewards", 
                              data = { "email": order_form.cleaned_data['email'], 
                                       "order_total": order_form.cleaned_data['order_total'] 
                                     })
                return HttpResponseRedirect('/rewards')

            # handle search form
            elif 'search-button' in request.POST and search_form.is_valid():
                response = requests.post("http://rewardsservice:7050/customer/get_rewards",
                              data = { "email": search_form.cleaned_data['email']})
                
                search_result = response.json()
                if search_result.get('message', None):
                    context['search_error'] = {'message': search_result['message']}
                else:
                    context['customer_data'] = [search_result]

                # Display forms and rewards info
                context['order_form'] = OrderForm()
                context['search_form'] = SearchForm()
                context['rewards_data'] = self.rewards

                # Show button to return to full user list
                context['show_reset_button'] = True

                return TemplateResponse(
                    request,
                    self.template_name,
                    context
                )