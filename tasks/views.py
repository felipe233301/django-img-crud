from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import Task

from django.db import IntegrityError

# Create your views here.

def home(request):
    return render(request, 'home.html')





#CREATE
@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html',{
            'form': TaskForm
        })
    else:

        try:
            form = TaskForm(request.POST,request.FILES)
            
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html',{
                'form': TaskForm,
                'error': 'please provide valid data'
            })

#READ
@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user,datecompleted__isnull = True)
    return render(request, 'tasks.html', {'tasks': tasks,'tasks_compl':'tru'})
@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user,datecompleted__isnull = False).order_by
    ('-date_completed')
    return render(request, 'tasks.html', {'tasks': tasks,'tasks_compl':'fal'})


#detail and updating (Read and Update)
@login_required
def task_detail(request,task_id):
    task = get_object_or_404(Task,pk=task_id,user=request.user)
    
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html',{'task': task,'form':form})
    else:
        try:
            form = TaskForm(request.POST,request.FILES, instance=task)

            if form.is_valid():  # Verificar si el formulario es válido
                form.save()  # Guardar la tarea actualizada
                return redirect('tasks')
            else:
                return render(request, 'task_detail.html', {
                    'task': task,
                    'form': form,
                    'error': 'Formulario no válido, por favor corrige los errores.'
                })            
            
        
        except ValueError:
            return render(request, 'task_detail.html',{
                'task': task,
                'form':form,
                'error': "Error updating task"
            })


@login_required
def complete_task(request,task_id):
    task = get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
       
#Detele
@login_required
def delete_task(request,task_id):
    task = get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method == 'POST':

        task.delete()
        return redirect('tasks')    



def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html',{
        'form' : UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                #register user
                user = User.objects.create_user(username=request.POST['username'], 
                password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('tasks')
            
            except IntegrityError:
                return render(request, 'signup.html',{
                    'form' : UserCreationForm,
                    'error': 'Username already exists'
                })
        
        return render(request, 'signup.html',{
            'form' : UserCreationForm,
            'error': 'Password do not match'
        })
    
@login_required    
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request,username=request.POST['username'],
            password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{
                'form': AuthenticationForm,
                'error': 'User or Password is incorrect'
            })
        else:
            login(request,user)
            return redirect('tasks')
        




