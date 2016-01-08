from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from django.core.urlresolvers import reverse_lazy

from .models import Department, Product, Review

# Create your views here.
def home(request):
    return render(request, 'home.html', {'departments': list(Department.objects.all())})
    
class DepartmentList(ListView):
    model = Department
    
    template_name = 'home.html'
    

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