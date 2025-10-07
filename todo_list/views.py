from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from urllib.parse import urlencode
from .models import Task, Category
from .forms import TaskForm

@login_required
def main_page(request):
    sort_by = request.GET.get('sort', 'due_date')
    if sort_by not in ('due_date', 'title', 'status'):
        sort_by = 'due_date'

    q = request.GET.get('q', '')
    selected_category = request.GET.get('category', '')

    # If you don’t have a custom manager with for_user/search, replace the next 4 lines:
    # tasks = Task.objects.for_user(request.user)
    tasks = Task.objects.filter(user=request.user)
    if selected_category:
        try:
            tasks = tasks.filter(category_id=int(selected_category))
        except (TypeError, ValueError):
            selected_category = ''
    if q:
        # If you don’t have .search(), use: tasks = tasks.filter(title__icontains=q)
        tasks = tasks.filter(title__icontains=q)

    tasks = tasks.order_by(sort_by)
    categories = Category.objects.order_by('name')

    return render(
        request,
        'index.html',
        {
            'tasks': tasks,
            'categories': categories,
            'selected_category': selected_category,
            'sort_by': sort_by,
            'q': q,
        },
    )

def task_list(request):
    params = request.GET.urlencode()
    url = reverse('main')
    return redirect(f"{url}?{params}" if params else url)

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('main')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('main')
    return render(request, 'task_confirm_delete.html', {'task': task})

@require_POST
@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.status = 'completed'
    task.save()
    return redirect('main')

@login_required
def task_search(request):
    # Redirect to main with q (and preserve category/sort if present)
    q = request.GET.get('q', '')
    args = {}
    if q:
        args['q'] = q
    cat = request.GET.get('category')
    if cat:
        args['category'] = cat
    sort = request.GET.get('sort')
    if sort:
        args['sort'] = sort
    url = reverse('main')
    return redirect(f"{url}?{urlencode(args)}" if args else url)


