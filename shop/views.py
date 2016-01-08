from django.shortcuts import render
from django.views.generic import ListView, CreateView

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