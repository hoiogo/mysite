from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, resolve_url, get_object_or_404 
from .mixins import OnlyYouMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy # 追加
from django.views.generic import DetailView, UpdateView, CreateView, ListView,DeleteView
from .forms import UserForm, ListForm, CardForm, CardCreateFromHomeForm
from . models import List,  Card


def index(request):
    return render(request, "memo/index.html")


@login_required
def home(request):
    return render(request, "memo/home.html")


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user_instance = form.save()
            login(request, user_instance)
            return redirect("memo:home")
    else:
        form = UserCreationForm()
        context = {
            "form": form
        }
    return render(request, 'memo/signup.html', context)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "memo/users/detail.html"


class UserUpdateView(OnlyYouMixin, UpdateView):
    model = User
    template_name = "memo/users/update.html"
    form_class = UserForm

    def get_success_url(self):
        return resolve_url('memo:users_detail', pk=self.kwargs['pk'])


class ListCreateView(LoginRequiredMixin, CreateView):
    model = List
    template_name = "memo/lists/create.html"
    form_class = ListForm
    success_url = reverse_lazy("memo:lists_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ListListView(LoginRequiredMixin, ListView):
    model = List
    template_name = "memo/lists/list.html"
    

class ListDetailView(LoginRequiredMixin, DetailView):
    model = List
    template_name = "memo/lists/detail.html"

class ListUpdateView(LoginRequiredMixin, UpdateView):
    model = List
    template_name = "memo/lists/update.html"
    form_class = ListForm
    success_url = reverse_lazy("memo:home")

    def get_success_url(self):
        return resolve_url('memo:lists_detail', pk=self.kwargs['pk'])
class ListDeleteView(LoginRequiredMixin, DeleteView):
    model = List
    template_name = "memo/lists/delete.html"
    success_url = reverse_lazy("memo:home")

class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    template_name = "memo/cards/create.html"
    form_class = CardForm
    success_url = reverse_lazy("memo:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CardListView(LoginRequiredMixin, ListView):
    model = Card
    template_name = "memo/cards/list.html"


class CardDetailView(LoginRequiredMixin, DetailView):
    model = Card
    template_name = "memo/cards/detail.html"

class CardUpdateView(LoginRequiredMixin, UpdateView):
    model = Card
    template_name = "memo/cards/update.html"
    form_class = CardForm

    success_url = reverse_lazy("memo:home")

class CardDeleteView(LoginRequiredMixin, DeleteView):
    model = Card
    template_name = "memo/cards/delete.html"
    success_url = reverse_lazy("memo:home")


class HomeView(LoginRequiredMixin, ListView):
    model = List
    template_name = "memo/home.html"

class CardCreateFromHomeView(LoginRequiredMixin, CreateView):
    model = Card
    template_name = "memo/cards/create.html" 
    form_class = CardCreateFromHomeForm
    success_url = reverse_lazy("memo:home")

    def form_valid(self, form):
        list_pk = self.kwargs['list_pk']
        list_instance = get_object_or_404(List, pk=list_pk)
        form.instance.list = list_instance
        form.instance.user = self.request.user
        return super().form_valid(form)