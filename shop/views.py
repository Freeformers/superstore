from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, FormView, TemplateView
from django.core.urlresolvers import reverse_lazy

from .models import Department, Product, Review
from .forms import ProductSearchForm

# Create your views here.
# def home(request):
    
#     search_form = ProductSearchForm()
    
#     return render(request, 'home.html', {
#         'departments': list(Department.objects.all()),
#         'search_form': search_form,
#     })
    
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