from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('<int:id_folder>', views.index, name='index'),
    path('files/<int:file_id>', views.files, name='files'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('new_folder/', views.new_folder, name='new_folder'),
    path('new_file/', views.new_file, name='new_file'),
    path('logout/', views.logout_user, name='logout'),
    path('delete/', views.delete, name='delete'),
    path('edit/<file>', views.edit_file, name='edit_file'),
    path('rename_file/', views.rename_file, name='rename_file'),
    path('rename_folder/', views.rename_folder, name='rename_folder'),
    path('create_file/', views.create_file, name='create_file'),
    path('folder/<id>', views.download_folder, name="download_folder"),
    path('send_folder/', views.send_folder, name='send_folder'),
    path('show/<id>', views.show, name='show'),
]