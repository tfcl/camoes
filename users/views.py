from django.shortcuts import render,redirect

from django.contrib import messages
from .forms import UserRegisterForm, ProfileCreateForm
from django.views.generic import ListView, UpdateView
from django.contrib.auth.models import User
from .models import Profile

def register(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        form1 = ProfileCreateForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            messages.success(request, f'Conta criada para {username}!')
            if form1.is_valid():
                profile = form1.save(commit=False)
                profile.user = user
                profile.save()
                
                return redirect('camoes-home')
            else:
                user.delete()
    else:
        form1 = ProfileCreateForm()
        form = UserRegisterForm()

    return render(request, 'users/register.html',{'form':form,'form1':form1})

class UserListView(ListView):
    model=User
    template_name='users/user_list.html'
    context_object_name='users'
    paginate_by=5


class UserUpdateView(UpdateView):
    model=User
    fields=['email']
    template_name='users/user-update.html'
