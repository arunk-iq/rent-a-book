import json
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import RentalForm
from .models import Book, Rental
from .utility import get_book_details
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator
from datetime import datetime
from django.utils import timezone


User = get_user_model()


#customized login required
class StaffCheckMixin(UserPassesTestMixin):
    login_url = '/login/'

    def test_func(self):
        return self.request.user.is_staff


class StaffHomeView(StaffCheckMixin, TemplateView):
    '''This page can be used as dashboard'''
    template_name = 'base.html' 


class StudentListView(StaffCheckMixin, ListView):
    model = User
    template_name = 'student_list.html'  # The template to render
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        # Filter users who are not admins (i.e., both is_staff and is_superuser are False)
        return User.objects.filter(is_staff=False, is_superuser=False)


class RentalListView(StaffCheckMixin, View):
    '''List all books already rented with their rent value'''
    def post(self, request):
        user_id = request.POST.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            rental_list = list(Rental.objects.filter(user=user))#.values("book__title",'rented_on',
                #'return_date','rental_cost')
            context={'rentals':rental_list, 'is_staff':True}
            return render(request, "rental_list.html", context)
        except Exception as e:
            print('e',e)
            # Change redirect to Student list with error
            return render(request, "rental_list.html")


class NewRental(StaffCheckMixin, View):
    def post(self,request):
        user_id = request.POST.get('user_id')
        try:
            context = {
                'user_id':user_id,
            }
            return render(request, "new_rental.html", context)
        except:
            # Change redirect to Student list with error
            return redirect("rental_details")


class SearchBookView(StaffCheckMixin, View):
    '''List all books already rented with their rent value'''
    def post(self, request):
        book_name = request.POST.get('book_name')
        book_list = get_book_details(book_name)
        return HttpResponse(json.dumps(book_list))


class SaveRentalView(StaffCheckMixin, View):
    '''List all books already rented with their rent value'''
    def post(self, request):
        form = RentalForm(request.POST)
        if form.is_valid():
            book = self.save_book_details(form.cleaned_data['selectedBook'])
            user_obj = self.get_user_obj(form.cleaned_data['userId'])
            rented_date = form.cleaned_data['rentedDate']
            return_date = form.cleaned_data['returnDate']
            rental_obj = Rental(user=user_obj,
                                book=book,
                                rented_on=rented_date,
                                return_date=return_date)
            rental_obj.save()
            messages.error(self.request, 'rental details updated')
            return redirect(reverse_lazy('student_list'))

    def put(self, request):
        """for updating"""
        try:
            data = json.loads(request.body)
            rental_obj = Rental.objects.get(id=data.get('rental_id'))
            return_date = datetime.strptime(data.get('return_date'),'%Y-%m-%d')
            timezone.make_aware(return_date)
            rental_obj.return_date = timezone.make_aware(return_date)
            rental_obj.save()
            return HttpResponse(json.dumps({'status':True, 
                                    'message':'Update Successful', 
                                    "rental_cost":"{:.2f}".format(rental_obj.rental_cost)}))
        except:
            return HttpResponse(json.dumps({'status':False, 'message':'Update Failed'}))

    def save_book_details(self, book_details):
        book_obj, created = Book.objects.update_or_create(
                                title=book_details['title'],
                                authors="|".join(book_details['author_name']),
                                defaults={
                                    'page_count':book_details['number_of_pages']
                                }
                            )
        return book_obj

    def get_user_obj(self, user_id):
        return User.objects.get(id=user_id)




class StudentHomeView(View):
    '''List all books already rented with their rent value'''
    def get(self, request):
        try:
            rental_list = list(Rental.objects.filter(user=request.user))#.values("book__title",'rented_on',
                #'return_date','rental_cost')
            context={'rentals':rental_list,}
            return render(request, "rental_list.html", context)
        except:
            return render(request, "rental_list.html")
