from django.shortcuts import render
from django.shortcuts import render, redirect
from . import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Staff, Attendance
from .serializers import StaffSerializer, AttendanceCreateSerializer
from django.contrib.auth.models import User



# Create your views here.
def home(request):
    context = {}
    return render(request,"index.html",context)

# ---------STAFF-------------

# 
# def staff_list(request):
#     staff = models.Staff.objects.all()
#     context = {'staff':staff}
#     return render(request, 'staff/list.html', context)



def staff_create(request):
    department = models.Department.objects.all()
    print(request.POST)
    if request.method == 'POST':
        models.Staff.objects.create(first_name = request.POST['name'],
                                    last_name = request.POST['last_name'],
                                    phone_number = request.POST['phone_number'],
                                    department_id = request.POST['department_id'],
                                    profile_image = request.FILES.get('profile_image'),
                                    email = request.POST['email'],
                                    adress = request.POST['adress'],
                                    )
        return redirect('staff_list')
    context = {'department':department}
    return render(request, 'staff/create.html',context)


def staff_update(request, id):
    staff = models.Staff.objects.get(id=id)
    department = models.Department.objects.all()
    if request.method == 'POST':
        if request.FILES.get('profile_image'):
            staff.profile_image = request.FILES.get('profile_image')
        staff.first_name = request.POST['name']
        staff.last_name = request.POST['last_name']
        staff.phone_number = request.POST['phone_number']
        staff.department_id = request.POST['department_id']
        staff.email = request.POST['email']
        staff.adress = request.POST['adress']
        staff.save()
        return redirect('staff_list')
    context = {
        'staff': staff,
        'department': department
    }
    return render(request, 'staff/update.html', context)


def staff_delete(request, id):
    queryset = models.Staff.objects.get(id=id)
    queryset.delete()
    print(request.POST)
    return redirect('staff_list')


# ---------AUTH-------------
def log_in(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request,'auth/login.html')
        except:
            return redirect('home')
    return render(request, 'auth/login.html')


def log_out(request):
    logout(request)
    return redirect('home')

@api_view(['GET'])
def staff_list(request):
    staff = Staff.objects.all()
    serializer = StaffSerializer(staff, many=True)
    return Response(serializer.data)

@api_view(['POST','GET'])
def attendance_create(request):
    serializer = AttendanceCreateSerializer(data=request.data)
    if serializer.is_valid():
        staff_id = serializer.validated_data['id']
        staff = get_object_or_404(Staff, id=staff_id)
        Attendance.objects.create(staff=staff)
        return Response({'message': 'Davomat muvaffaqiyatli yaratildi.'}, status=201)
    return Response(serializer.errors, status=400)

def attendance_list(request):
    attendances = Attendance.objects.all()
    return render(request, 'attendance/list.html', {'attendances': attendances})

def edit_user(request):
    if request.method == 'POST':
        new_email = request.POST['email']
        new_username = request.POST['username']
        superuser = get_object_or_404(User.objects.get(username=request.user.username))
        superuser.email = new_email
        superuser.username = new_username
        superuser.save()
        return redirect('home')
    else:
        superuser = User.objects.get(username=request.user.username)
        return render(request, 'user/edit.html', {'superuser': superuser})