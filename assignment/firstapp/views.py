from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Students

@csrf_exempt
def get_students(request):
    if request.method == "GET":
        students = list(Students.objects.all())
        if not students:
            return JsonResponse({"message": "No students found"}, status=404)
        fields = [f.name for f in students[0]._meta.get_fields()]
        result = [{field :  getattr(obj, field) for field in fields} for obj in students]
        return JsonResponse({"students": result})

@csrf_exempt
def add_student(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if 'id' in data and (data['id'] == '' or data['id'] is None):
            data.pop('id')
        student = Students.objects.create(**data)
        return JsonResponse({"message": "Student added", "student": data})

@csrf_exempt
def edit_student(request, student_id):
    student = get_object_or_404(Students, id=student_id)
    if request.method == "PUT":
        data = json.loads(request.body)
        for field, value in data.items():
            setattr(student, field, value)
        student.save()
        return JsonResponse({"message": "Student updated"})

@csrf_exempt
def delete_student(request, student_id):
    student = get_object_or_404(Students, id=student_id)
    if request.method == "DELETE":
        student.delete()
        return JsonResponse({"message": "Student deleted"})
    

def home_view(request):
    return render(request, 'index.html')
