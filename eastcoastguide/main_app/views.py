from django.contrib.auth import login
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from .models import Restaurant, Comment, User
from django.contrib.auth.mixins import LoginRequiredMixin

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form, 'error_message': 'Invalid sign up - try again'})

class Home(TemplateView):
    template_name = 'home.html'
    
class About(TemplateView):
    template_name = 'about.html'

class RestaurantsNYIndex(ListView):
    model = Restaurant
    template_name = 'restaurants/index.html'
    
    def get_queryset(self):
        return self.model.objects.filter(location='New York')
    
class RestaurantsMAIndex(ListView):
    model = Restaurant
    template_name = 'restaurants/index.html'
    
    def get_queryset(self):
        return self.model.objects.filter(location='Massachusetts')


class RestaurantCreate(CreateView):
    model = Restaurant
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class CommentCreate(CreateView):
    model = Comment
    fields = '__all__'

#for the detail class in order to get it to work, the comments model will need to have the foreign key! I can always adjust accordingly once the models are created if there are any bugs :)
class RestaurantDetail(DetailView):
    model = Restaurant
    template_name = 'restaurants/detail.html'
    context_object_name = 'restaurant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = self.get_object()
        context['comments'] = restaurant.comment.all()
        return context
    