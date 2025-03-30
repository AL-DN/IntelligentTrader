from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Post
from .utils import fetch_and_cache_ticker_data  # Utility to fetch financial data
import pandas as pd
from joblib import load
import os
from django.conf import settings

class PostListView(ListView):
    model=Post
    template_name='predictions/home.html' #  <app>/<model>_<viewtype>.html
    context_object_name='posts' # context
    ordering=['-date_created']
    paginate_by = 10

class UserPostListView(ListView):
    model=Post
    template_name='predictions/user_posts.html' #  <app>/<model>_<viewtype>.html
    context_object_name='posts' # context
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_created')

class PostDetailView(DetailView):
    model=Post
    # context_object_name=object
    # template_name = post_detail.html

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['ticker']

    def form_valid(self, form):
        form.instance.author = self.request.user
        ticker = form.cleaned_data['ticker']
        
        try:
            # Fetch and cache ticker data
            ticker_data = fetch_and_cache_ticker_data(ticker)

            # Load the model using the full path
            model_path = os.path.join(settings.BASE_DIR,
                                      'predictions',
                                      'models',
                                      'rf.joblib')
            model = load(model_path)  # Now joblib will find it

            prediction = model.predict(ticker_data)
            
            # Save the prediction to the Post instance
            form.instance.fin_rep_score = prediction
        except Exception as e:
            # Handle errors (e.g., API failure, invalid data)
            form.add_error('ticker', f"Unable to fetch data for this ticker: {str(e)}")
            return self.form_invalid(form)

        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=Post
    fields = ['ticker','earning_report_score']
    # context_object_name=object
    # template_name = post_detail.html

    # overrides method so that
    # for the current form user is trying to submit
    # make its author the current logged in user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else: return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Post
    success_url='/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else: return False

def about(request):
    return render(request, 'predictions/about.html',context= {'ticker': 'About'})


