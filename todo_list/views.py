from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from allauth.account.forms import LoginForm, SignupForm  # add
from django.contrib import messages
from django.urls import reverse
from urllib.parse import urlencode

from .models import Task, Category
from .forms import TaskForm

def main_page(request):
    sort_by = request.GET.get('sort', 'due_date')
    if sort_by not in ('due_date', 'title', 'status'):
        sort_by = 'due_date'

    q = request.GET.get('q', '')
    selected_category = request.GET.get('category', '')

    tasks = Task.objects.filter(user=request.user) if request.user.is_authenticated else Task.objects.none()

    if selected_category:
        try:
            tasks = tasks.filter(category_id=int(selected_category))
        except (TypeError, ValueError):
            selected_category = ''

    if q:
        tasks = tasks.filter(title__icontains=q)

    tasks = tasks.order_by(sort_by)
    categories = Category.objects.order_by('name')

    context = {
        'tasks': tasks,
        'categories': categories,
        'selected_category': selected_category,
        'sort_by': sort_by,
        'q': q,
        # AllAuth forms for the modals:
        'login_form': LoginForm(),
        'signup_form': SignupForm(),
    }

    return render(request, 'index.html', context)

def task_list(request):
    # legacy alias -> keep any params and go back to main
    params = request.GET.urlencode()
    url = reverse('main')
    return redirect(f"{url}?{params}" if params else url)

def task_search(request):
    args = {}
    q = request.GET.get('q', '')
    cat = request.GET.get('category', '')
    sort = request.GET.get('sort', '')
    if q: args['q'] = q
    if cat: args['category'] = cat
    if sort: args['sort'] = sort
    url = reverse('main')
    return redirect(f"{url}?{urlencode(args)}" if args else url)

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, "Task created")
            return redirect('main')
    else:
        form = TaskForm()
    # If you prefer no separate page, you can swap this render for a redirect.
    return render(request, 'task_form.html', {'form': form, 'mode': 'create'})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated")
            return redirect('main')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form, 'mode': 'edit', 'task': task})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, "Task deleted")
        return redirect('main')
    # Minimal confirm page to ensure GET returns a response
    return render(request, 'task_confirm_delete.html', {'task': task})

@require_POST
@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.status = 'completed'
    task.save()
    messages.success(request, "Task completed")
    return redirect('main')

@require_POST
def ajax_login(request):
    """
    Validate with AllAuth's LoginForm and return JSON.
    On success: log the user in and return ok: true.
    On failure: 400 with a generic error message.
    """
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    form = LoginForm(data=request.POST, request=request)

    if form.is_valid():
        form.login(request)  # AllAuth logs the user in
        messages.success(request, "Logged in")  # will show once via toasts
        if is_ajax:
            return JsonResponse({"ok": True})
        # Non-AJAX fallback: go back to index, no JSON page
        return redirect('main')

    # Invalid credentials
    if is_ajax:
        return JsonResponse(
            {"ok": False, "message": "Incorrect password, please try again."},
            status=400,
        )
    # Non-AJAX fallback: show toast on index instead of AllAuth page
    messages.error(request, "Incorrect password, please try again.")
    return redirect('main')


