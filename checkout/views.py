from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ApplicationForm
from .models import Transaction, Application
from apartment.models import Apartment
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import datetime
import json

@login_required(login_url = 'login')
def thankyou(request):
    return render(request, 'apartment/thankyou_page.html')

@login_required(login_url = 'login')
def transaction(request):
    body = json.loads(request.body)
    application = Application.objects.get(user=request.user, application_number=body['applicationID'])

    transaction = Transaction(
        user = request.user,
        transaction_id = body['transactionID'],
        status = body['status'],
        fees = 5,
    )
    transaction.save()
    application.transaction = transaction
    application.is_ordered = True
    application.save()

    subject = 'Thankyou, Application received!'
    body = render_to_string('accounts/applicationConfirmation_template.html', {
        'user_details': request.user,
        'application': application,
    })
    
    email = request.user.email
    send_mail( subject, body, 'ysoni0303@gmail.com', [email], fail_silently=False)
    return render(request, 'apartment/thankyou_page.html')

@login_required(login_url = 'login')
def checkout(request, apartment_id):
    print('request', request)
    print('apartment_id', apartment_id)
    current_user = request.user
    apartment = Apartment.objects.get(id=apartment_id)
    url = request.META.get('HTTP_REFERER')
    print('apartmentapartment', apartment)
    if request.method == 'POST':
        print('IT IS A POST REQUEST')
        form = ApplicationForm(request.POST)
        if form.is_valid():
            data = Application()
            data.user = current_user
            data.apartment = apartment
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.country = form.cleaned_data['country']
            data.fees = 5
            data.save()

            application_number = generateApplicationID(data.id)
            data.application_number = application_number
            data.save()

            application = Application.objects.get(user=current_user, application_number=application_number)

            context = {
                'application': application,
                'apartment': apartment
            }
            return render(request, 'apartment/transaction.html', context)
    else:
        form = ApplicationForm()
    context = {
        'form': form,
        'apartment_id':apartment_id
    }
    return render(request, 'apartment/checkout.html', context)

        

def generateApplicationID(id):
    current_year = int(datetime.date.today().strftime('%Y'))
    current_day = int(datetime.date.today().strftime('%d'))
    current_month = int(datetime.date.today().strftime('%m'))
    date = datetime.date(current_year,current_month,current_day)
    current_date = date.strftime("%Y%m%d")
    application_number = current_date + str(id)
    return application_number