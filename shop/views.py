import json
import requests

from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, FormView, TemplateView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse

from .models import Department, Product, Review
from .forms import ProductSearchForm
from .backend import handle_purchase, steps, WAREHOUSE_PHONE, SECRET_CODE

    
class DepartmentList(ListView):
    model = Department
    
    template_name = 'home.html'
        
        
class ProductSearch(TemplateView):
    template_name = 'shop/search.html'
    
    def get_context_data(self, **kwargs):
        context = super(ProductSearch, self).get_context_data(**kwargs)
        
        form = ProductSearchForm(self.request.GET)
        context['form'] = form
        
        if form.is_valid():
            criteria = form.cleaned_data
            
            query = Product.objects.all().order_by('name')
            
            if criteria['department']:
                query = query.filter(department=criteria['department'])
                
            if criteria['name']:
                query = query.filter(name__icontains=criteria['name'])
                
            if criteria['colour'] and criteria['colour'] != '0':
                query = query.filter(colour=criteria['colour'])
            
            context['results'] = query
            
        else:
            context['results'] = []
        
        return context
    

class CreateDepartment(CreateView):
    model = Department
    fields = ['name', 'image_url']
    success_url = '/'
    
    
class ShopDepartment(DetailView):
    model = Department
    
    
class CreateProduct(CreateView):
    model = Product
    fields = ['name', 'description', 'image_url', 'department', 'colour']
    success_url = '/'
    
    def get_success_url(self):
        return reverse_lazy('shop-department', kwargs={'pk': self.object.department_id})
        
        
class ShopProduct(DetailView):
    model = Product
    
    def post(request, *args, **kwargs):
        raise Exception()

    
def check_steps(request, steps, product_name):
    better_labels = {
        'start_purchase': 'Start purchase process',
        'check_inventory': 'Check warehouse inventory',
        'calculate_price': 'Calculate price of order',
        'take_payment': 'Take payment from customer account',
        'inform_warehouse': 'Inform warehouse to dispatch purchase',
        'notify_customer': 'Notify customer of successful purchase',
        'update_sales_tracker': 'Log purchase in the sales tracker',
        'finish_purchase': 'Complete purchase process',
    }
    step_nodes = [{'id': i, 'label': better_labels.get(step, step), 'shape': 'square'} for (i, step) in enumerate(steps)]
    
    problem = None
    bad_step = None
    
    if steps[0] != 'start_purchase':
        problem = 'Must begin with start_purchase'
        bad_step = 0
    elif steps[-1] != 'finish_purchase':
        problem = 'Must end with finish_purchase'
        bad_step = len(steps) - 1
    elif 'check_inventory' not in steps:
        problem = 'Must check stock level'
        bad_step = 1
    elif 'take_payment' not in steps:
        problem = 'Must take payment at some point!'
        bad_step = 1
    elif steps.index('check_inventory') > steps.index('take_payment'):
        problem = 'Inventory needs to be checked before taking money'
        bad_step = steps.index('take_payment')
    elif 'calculate_price' not in steps:
        problem = 'You must calculate how much to charge'
        bad_step = 1
    elif steps.index('calculate_price') > steps.index('take_payment'):
        problem = 'Price calculation needs to happen before charging'
        bad_step = steps.index('take_payment')
    elif 'inform_warehouse' not in steps:
        problem = 'Warehouse team must be informed of the purchase'
        bad_step = steps.index('take_payment')
    elif steps.index('take_payment') > steps.index('inform_warehouse'):
        problem = 'The warehouse should only be informed after taking payment'
        bad_step = steps.index('inform_warehouse')
    elif 'notify_customer' not in steps:
        problem = 'Customer must receive confirmation of the purchase'
        bad_step = steps.index('take_payment')
    elif steps.index('take_payment') > steps.index('notify_customer'):
        problem = 'The customer should only get confirmation after payment is taken'
        bad_step = steps.index('notify_customer')
    elif 'update_sales_tracker' not in steps:
        problem = 'Successful purchases should be logged'
        bad_step = steps.index('take_payment')
    elif steps.index('take_payment') > steps.index('update_sales_tracker'):
        problem = 'Purchase logging should only happen after taking payment'
        bad_step = steps.index('update_sales_tracker')
    
    res = []
    for (i, step_node) in enumerate(step_nodes):
        new_edges = []
        if i > 0:
            new_edges.append(
                {'from': step_node['id'] - 1, 'to': step_node['id'], 'arrows': 'to'}
            )
            
        if bad_step != None and bad_step <= i:
            step_node['color'] = 'red'
        
        res.append({
            'new_nodes': [step_node],
            'new_edges': new_edges,
        })
        
    if problem != None:
        res[-1]['fail'] = True
        res[-1]['fail_message'] = problem
    else:
        res[-1]['success'] = True
        
        requests.post(
            'https://api.twilio.com/2010-04-01/Accounts/AC2823ba83b1055dff4ed6788cfed35f0b/Messages.json',
            auth=('AC2823ba83b1055dff4ed6788cfed35f0b', SECRET_CODE),
            data={
                'To': MY_PHONE,
                'From': '+441432233633',
                'Body': 'Incoming order for {}'.format(product_name),
            }
        )
    
    return res
        
def start_purchase(request):
    product_id = int(request.POST['product_id'])
    product = Product.objects.get(id=product_id)
    
    steps[:] = []
    
    handle_purchase()
    
    converted_steps = check_steps(request, steps, product.name)
    
    return render(request, 'shop/start_purchase.html', {
        'product': product,
        'steps_json': json.dumps(converted_steps),
    })