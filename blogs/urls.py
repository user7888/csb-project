from django.urls import path

from . import views

app_name = 'blogs'
urlpatterns = [
    # ex: /polls/
    path('', views.indexView, name='index'),
    # ex: /polls/5/
    path('<int:blog_post_id>/', views.detailView, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.resultsView, name='results'),
    # ex: /polls/5/vote/
    #path('<int:question_id>/vote/', views.voteView, name='vote'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('add_question/', views.addBlogPostView, name='add_blogpost'),
    path('blog_posts/', views.BlogPostsView, name='blog_posts'),
    path('blog_posts/<int:blog_post_id>/delete', views.deleteView, name='delete'),
]