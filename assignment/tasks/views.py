import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from functools import wraps
from .models import Task
from django.utils.dateparse import parse_datetime

# Decorator to check if user is logged in
def login_required_api(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper

@csrf_exempt
def register_api(request):
    if request.method != 'POST':
        print(request.method)
        return JsonResponse({'error': 'POST request required'}, status=400)

    try:
        data = json.loads(request.body)

        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
    except:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if not username or not password or not confirm_password:
        return JsonResponse({'error': 'Missing fields'}, status=400)

    if password != confirm_password:
        return JsonResponse({'error': 'Passwords do not match'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)
    
    user = User.objects.create_user(username=username, password=password)
    user.save()

    return JsonResponse({'message': 'User registered successfully'})

@csrf_exempt
def login_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
    except:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'Login successful'})
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

@csrf_exempt
@login_required_api
def logout_api(request):
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'})

@csrf_exempt
@login_required_api
def protected_api(request):
    return JsonResponse({'message': f'Hello, {request.user.username}. This is a protected API endpoint.'})




@csrf_exempt
@login_required_api
def get_all_tasks(request):
    if request.method != 'GET':
        return HttpResponseBadRequest("GET method required")
    id  = User.objects.get(username=request.user).id
    tasks = Task.objects.filter(user_id=request.user).values()
    return JsonResponse(list(tasks), safe=False)


@csrf_exempt
@login_required_api
def mark_task_completed(request, task_id):
    if request.method != 'POST':
        return HttpResponseBadRequest("POST method required")

    try:
        task = Task.objects.get(id=task_id, user=request.user)
        task.status = "completed"
        task.save()
        return JsonResponse({'message': 'Task marked as completed'})
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)


@csrf_exempt
@login_required_api
def add_task(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("POST method required")

    try:
        data = json.loads(request.body)
        id  = User.objects.get(username=request.user).id
        print(id)


        # id = 4
        task = Task.objects.create(
            user_id=id,
            subject=data['subject'],
            description=data['description'],
            module=data['module'],
            assigned_to=data['assigned_to'],
            approver=data['approver'],
            estimated_minutes=int(data['estimated_minutes']),
            start_datetime=parse_datetime(data['start_datetime']),
            end_datetime=parse_datetime(data['end_datetime']),
            source=data['source'],
            out_of_duties_task=bool(data['out_of_duties_task']),
            priority=data.get('priority', 'medium'),
            status=data.get('status', 'pending'),
            completion_percentage=data.get('completion_percentage', 0),
        )

        return JsonResponse({'message': 'Task created', 'task_id': task.id})
    except KeyError as e:
        return JsonResponse({'error': f'Missing field {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@csrf_exempt
@login_required_api
def get_user_name(request):
    if request.method != 'GET':
        return HttpResponseBadRequest("GET method required")

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    return JsonResponse({'username': request.user.username})