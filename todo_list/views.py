from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Task, Category
from .forms import TaskForm

@login_required
def main_page(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'index.html', {'tasks': tasks})

def task_list(request):
    sort_by = request.GET.get('sort', 'due_date')  # Default sort
    valid_sorts = ['status', 'due_date']
    if sort_by not in valid_sorts:
        sort_by = 'due_date'
    tasks = Task.objects.filter(user=request.user).order_by(sort_by)
    return render(request, 'index.html', {'tasks': tasks, 'sort_by': sort_by})

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})

def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task_confirm_delete.html', {'task': task})

def tasks_by_category(request, category_name):
    tasks = Task.objects.filter(user=request.user, category__name=category_name)
    return render(request, 'task_list.html', {'tasks': tasks, 'selected_category': category_name})

@require_POST
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.status = 'completed'
    task.save()
    return redirect('main')


