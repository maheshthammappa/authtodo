from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic.edit import DeleteView

from django.contrib.auth.views import LoginView
from django.contrib.auth import login

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from .forms import RegisterForm
from django.views import View

class TaskToggle(View):
    def get(self, request, pk):
        task = get_object_or_404(Task, id=pk)

        task.complete = not task.complete   # switches True ↔ False
        task.save()

        return redirect('task_list')

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'home/register.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("task_list")
        return super().dispatch(request, *args, **kwargs)
    

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    
    def get_queryset(self):
        search_input = self.request.GET.get('search_area', '')

        queryset = Task.objects.filter(user=self.request.user)

        if search_input:
            queryset = queryset.filter(title__icontains=search_input)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['count'] = self.get_queryset().filter(complete=False).count()
        context['search_input'] = self.request.GET.get('search-area', '')

        return context
    
    
    
class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    template_name = 'home/task_create.html'
    success_url = reverse_lazy('task_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    template_name = 'home/task_create.html'
    success_url = reverse_lazy('task_list')
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    template_name = 'home/task_delete.html'
    success_url = reverse_lazy('task_list')
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
class CustomLogin(LoginView):
    template_name = 'home/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('task_list')