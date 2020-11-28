from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import *
from .rawSQL import *
import datetime
from index.decorators import *
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
@isNotLoggedIn
@isAdminLogin
def adminLoginView(request):
    if request.session.get("admin"):
       return redirect('adminMainPage')
    context = {}
    form = adminLoginForm()
    if request.method == "POST":
        form = adminLoginForm(request.POST)
        if form.is_valid():
            roll_number = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if roll_number == 'admin' and password == 'admin':
                request.session.flush()
                request.session['admin'] = 'admin'
                return redirect('adminMainPage')
        context['error'] = "Invalid Credentials"
    context['form'] = adminLoginForm()
    return render(request, 'admin/adminLogin.html', context)


@isLoggedIn
@isAdmin
def adminMainPageView(request):
    context = {}
    return render(request, 'admin/adminMainPage.html', context)



@isLoggedIn
@isAdmin
def addCourseStudentView(request):
    context = {}
    allCourses = getAllCourses()
    context['allCourses'] = allCourses
    # allStudents = getAllStudents()
    # context['allStudents'] = allStudents
    now = datetime.datetime.now()
    context["yearList"] = range(now.year - 10, now.year)
    if request.method == "GET":
        return render(request, 'admin/addCourseStudent.html', context)
    if request.method == "POST":
        studentRollNumber = request.POST.get('rollNumber')
        selectedCourse = request.POST.get('course')
        studentGPA = request.POST.get('GPA')
        selectedSemester = request.POST.get('semester')
        selectedSemesterYear = request.POST.get('semesterYear')
        insertion = insertStudentCourseInfo(studentRollNumber, selectedCourse, studentGPA, selectedSemester, selectedSemesterYear)
        context["update"] = insertion
        return render(request, 'admin/addCourseStudent.html', context)        


@isLoggedIn
@isAdmin
def removeCourseStudentHelperView(request):
    context = {}
    if request.method == "GET":
        return render(request, 'admin/removeCourseStudentHelper.html', context)
    if request.method == "POST":
        studentRollNumber = request.POST.get('rollNumber')
        cousesTakenByStudent = getCoursesTaken(studentRollNumber)
        context["rollNumber"] = studentRollNumber
        context["allCourses"] = cousesTakenByStudent
        return render(request, 'admin/removeCourseStudent.html', context)


@isLoggedIn
@isAdmin
def removeCourseStudentView(request):
    context = {}
    if request.method == "GET":
        return redirect("removeCourseStudentHelper")
    if request.method == "POST":
        studentRollNumber = request.POST.get('rollNumber')
        course = request.POST.get('course')
        result = removeCourse(studentRollNumber, course)
        context["update"] = result
        cousesTakenByStudent = getCoursesTaken(studentRollNumber)
        context["rollNumber"] = studentRollNumber
        context["allCourses"] = cousesTakenByStudent
        return render(request, 'admin/removeCourseStudent.html', context)

@isLoggedIn
@isAdmin
def addInstructorView(request):
    context = {}
    if request.method == "GET":
        return render(request, 'admin/addInstructor.html', context)
    if request.method == "POST":
        insID = request.POST.get("instructorID")
        name = request.POST.get("name")
        department = request.POST.get("department")
        rating = request.POST.get("rating")
        school = request.POST.get("school")
        result = insertInstructorInfo(insID, name, department, rating, school)
        context["update"] = result
        return render(request, 'admin/addInstructor.html', context)


@isLoggedIn
@isAdmin
def removeInstructorView(request):
    context = {}
    if request.method == "GET":
        allInstructors = getAllInstructors()
        context['allInstructors'] = allInstructors
        return render(request, 'admin/removeInstructor.html', context)
    if request.method == "POST":
        insID = request.POST.get("instructor")
        result = removeInstructor(insID)
        allInstructors = getAllInstructors()
        context['allInstructors'] = allInstructors
        context["update"] = result
        return render(request, 'admin/removeInstructor.html', context)