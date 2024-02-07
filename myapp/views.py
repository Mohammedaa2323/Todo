from django.shortcuts import render,redirect
from django import forms
from myapp.models import Todo
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# Create your views here.

#         form of todo

class TodoForm(forms.ModelForm):
    class Meta:
        model=Todo
        exclude=("created_date","user_object")


#       todo list 
        

class TodoListView(View):
    def get(self,request,*args,**kwargs):
        qs=Todo.objects.filter(user_object=request.user)
        return render(request,"todo_list.html",{"data":qs})
    
#         todo creating
class TodocreateView(View):
    def get(self,request,*args,**kwargs):
        form=TodoForm()
        return render(request,"todo_add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=TodoForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            Todo.objects.create(**data,user_object=request.user)
            # form.save()
            return redirect("todo-list")
        else:
         return render(request,"todo_add.html",{"form":form})

#         todo detail

class TodoDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Todo.objects.get(id=id)
        return render(request,"todo_detail.html",{"data":qs})


#          delete view
class TodoDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Todo.objects.get(id=id).delete()
        return redirect("todo-list")
    


#       update view

class TodoUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_objects=Todo.objects.get(id=id)
        form=TodoForm(instance=todo_objects)
        return render(request,"todo_update.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_objects=Todo.objects.get(id=id)
        form=TodoForm(request.POST,instance=todo_objects)
        if form.is_valid():
            form.save()
            return redirect("todo-list")
        else:
            return render(request,"todo_update.html",{"form":form})


class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email","password"]

class SignupView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            print("added")
            return redirect("signin")
        else:
           return render(request,"register.html",{"form":form})


#       login form
        
class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

#       signup view

class SigninView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"signin.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            userobject=authenticate(request,username=u_name,password=pwd)
            if userobject:
                login(request,userobject)
                print("valid")
                return redirect("todo-list")
        print("invalid")
        return render(request,"signin.html",{"form":form})


class SignoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")