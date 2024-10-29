# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.StaffHomeView.as_view(), name='home'),
    path('student-list/', views.StudentListView.as_view(), name='student_list'),
    path('rental-details/', views.RentalListView.as_view(), name='rental_details'),
    path('new-rental/', views.NewRental.as_view(), name='new_rental'),
    path('search-book/', views.SearchBookView.as_view(), name='search_book'),
    path('save-rental/', views.SaveRentalView.as_view(), name='save_rental'),
    path('st-home/', views.StudentHomeView.as_view(), name='st_home'),
]