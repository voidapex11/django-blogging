from django.shortcuts import get_object_or_404, render
from django.views import generic

from .forms import CommentForm
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


def username_exists(username):
  return User.objects.filter(username=username).exists()


class PostList(generic.ListView):
  queryset = Post.objects.filter(status=1).order_by("-created_on")
  template_name = "index.html"
  paginate_by = 3


# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'post_detail.html'


def post_detail(request, slug, styles=None):
  template_name = "post_detail.html"
  post = get_object_or_404(Post, slug=slug)
  comments = post.comments.filter(active=True).order_by("-created_on")
  
  new_comment = None
  # Comment posted
  if request.method == "POST":
    comment_form = CommentForm(data=request.POST)
    if comment_form.is_valid():
      
      # Create Comment object but don't save to database yet
      new_comment = comment_form.save(commit=False)
      # Assign the current post to the comment
      
      new_comment.post = post
      new_comment.name = request.user.username
      new_comment.email = request.user.email
      
      # Save the comment to the database
      if request.user.is_authenticated:
        if request.user.is_active:
          new_comment.save()
          
      
  else:
    comment_form = CommentForm()

  return render(
      request,
      template_name,
      {
          "post": post,
          "comments": comments,
          "new_comment": new_comment,
          "comment_form": comment_form,
      },
  )
