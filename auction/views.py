from email.mime.multipart import MIMEMultipart

from django.contrib.auth.views import PasswordResetView
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.db.models import Q, Count, QuerySet

from JustBid import settings
from .forms import CustomerCreationForm, CustomerEditProfileForm, CustomerItemsForm, CustomerBidsForm, \
    CustomerEditItemsForm, CustomerRepostItemsForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
from .models import Item, Bid

###FOR PDF generation###
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import StringIO





def CustomerSignUp(request):
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))

        else:
            return render(request, 'registration/signup.html', {'form': form})
    else:
        form = CustomerCreationForm()
        return render(request, 'registration/signup.html', {'form': form})


##Password
class PasswordResetJBEmailView(PasswordResetView):
    PasswordResetView.extra_email_context = {'jb_site_name': 'Just Bid.com'}

# method for editing customer profile
@login_required()
def edit_customerProfile(request):
    if request.method == 'POST':
        form = CustomerEditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('auction:profile_preview'))
        else:
            return render(request, 'Edit_CustomerProfile.html', {'form': form})
    else:
        form = CustomerEditProfileForm(instance=request.user)
        return render(request, 'Edit_CustomerProfile.html', {'form': form})


#######################  ITEMS
# method to display customer items
def customerItemsList(request):
    items = Item.objects.filter(customer_id=request.user);
    return render(request, 'Customer_Itemslist.html', {'items': items})


# method to search for customer items
def customerItemSearch(request):
    pk = request.GET['item_search']
    itemsSearched = Item.objects.filter(~Q(customer_id=request.user),name__contains=pk,end_date__gt=datetime.now(),
                                    start_date__lte=datetime.now());
    itemsSearchedFlag = True
    print("itemsSearched------",itemsSearched)
    items_bidded = Item.objects.filter(bid_item_id__customer_id=request.user)
    trending_bids = None
    trendinBidsAll = None
    now = datetime.now()
    itemsSearchedString = pk
    return render(request, 'home.html', {'items': itemsSearched, 'now': now, 'items_bidded': items_bidded,
                                         'trending_bids': trending_bids, 'trending_bidsAll': trendinBidsAll,'itemsSearchedString':itemsSearchedString})

# method to display avaible bid items for the customer to bid
def customerItemsListToBid(request):
    if request.user.is_authenticated:
        items = Item.objects.filter(~Q(customer_id=request.user), end_date__gt=datetime.now(),
                                    start_date__lte=datetime.now())
        items_bidded = Item.objects.filter(bid_item_id__customer_id=request.user)
        print(items_bidded)
    else:
        items = None
        items_bidded = None
    itemAll = Item.objects.all()
    trendinBidsAll = Bid.objects.none()
    for eachiteam in itemAll:
        maxBid = Bid.objects.filter(item_id=eachiteam.id,).order_by('-amount').order_by('-time').first()
        if maxBid:
            trendinBidsAll|= Bid.objects.filter(id=maxBid.id)
    trending_bids = Bid.objects.all().select_related('item_id').order_by('-amount').order_by('-time')
    now = datetime.now()
    itemsSearchedString = ''
    return render(request, 'home.html', {'items': items, 'now': now, 'items_bidded': items_bidded,
                                         'trending_bids': trending_bids, 'trending_bidsAll': trendinBidsAll,'itemsSearchedString':itemsSearchedString})

# method to add customer Items
def addCustomerItems(request):
    if request.method == 'POST':
        form = CustomerItemsForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.customer_id = request.user
            instance.end_date = instance.start_date + timedelta(days=7)
            instance.save()
            return redirect(reverse('auction:customer_items'))
        else:
            return render(request, 'Customer_Itemsadd.html', {'form': form})
    else:
        form = CustomerItemsForm(instance=request.user)
        return render(request, 'Customer_Itemsadd.html', {'form': form})

# method to edit customer Items
def editCustomerItems(request, pk):
    item = Item.objects.filter(id=pk).first()
    if request.user.id != item.customer_id.id:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = CustomerEditItemsForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect(reverse('auction:customer_items'))
        else:
            return render(request, 'Customer_Itemsedit.html', {'form': form})
    form = CustomerEditItemsForm(instance=item)
    return render(request, 'Customer_Itemsedit.html', {'form': form})

# method to repost customer Items
def repostCustomerItems(request, pk):
    item = Item.objects.filter(id=pk).first()
    if request.user.id != item.customer_id.id:
        return HttpResponseForbidden()

    item.name = item.name + ' - Repost'
    if request.method == 'POST':
        form = CustomerRepostItemsForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.customer_id = request.user
            instance.end_date = instance.start_date + timedelta(days=7)
            instance.save()
            return redirect(reverse('auction:customer_items'))
        else:
            return render(request, 'Customer_Itemsedit.html', {'form': form})
    form = CustomerRepostItemsForm(instance=item)
    return render(request, 'Customer_Itemsedit.html', {'form': form})

# method to delete customer posted Items
def deleteCustomerItems(request, pk):
    item = Item.objects.filter(id=pk).first()
    if request.user.id != item.customer_id.id:
        return HttpResponseForbidden()

    item.delete()
    items = Item.objects.filter(customer_id=request.user)
    return render(request, 'Customer_Itemslist.html', {'items': items})

# method to check History of Bids the customer posted
def customerItemBidHistory(request, pk):
    bids = Bid.objects.filter(item_id_id=pk, item_id__customer_id=request.user).order_by('-time')
    return render(request, 'Customer_ItemBidHistory.html', {'bids': bids})

# method to make the winner for the bids by  the owner of customer
def customerBidWinner(request, pk):
    bid = Bid.objects.filter(id=pk).first()
    print('winner is', bid.customer_id, 'for item: ', bid.item_id.name)
    item = Item.objects.filter(id=bid.item_id.id).first()
    item.name = item.name + ' BID DONE'
    item.save()
    bids = Bid.objects.filter(item_id_id=bid.item_id.id, item_id__customer_id=request.user).order_by('-time')
    return render(request, 'Customer_ItemBidHistory.html', {'bids': bids})

####################### BIDS

# method to display bids lists of cutomer- My Bids
def customerBidsList(request):
    bids = Bid.objects.filter(customer_id=request.user).order_by('-time')
    return render(request, 'Customer_Bidslist.html', {'bids': bids})

# method to perform bid on an item
def customerBidNow(request, pk):
    now = datetime.now()
    item = Item.objects.filter(id=pk).first()
    if request.user.id == item.customer_id.id:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = CustomerBidsForm(request.POST, identifier=item)
        # form = CustomerBidsForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.customer_id = request.user
            bid.item_id = Item.objects.filter(id=pk).first()
            bid.time = datetime.now()
            bid.save()
            return redirect(reverse('auction:customer_bids'))
        else:
            return render(request, 'Customer_BidNow.html', {'item': item, 'form': form, 'now': now})
    else:
        form = CustomerBidsForm()
        return render(request, 'Customer_BidNow.html', {'item': item, 'form': form, 'now': now})

# method to rebid the bidded items by customer
def customerBidAgain(request, pk):
    item = Item.objects.filter(id=pk).first()
    if request.user.id == item.customer_id.id:
        return HttpResponseForbidden()
    mycurrentBid = Bid.objects.filter(customer_id_id=request.user.id, item_id=pk).order_by('-time').first().amount
    if request.method == 'POST':
        form = CustomerBidsForm(request.POST, identifier=item)
        # form = CustomerBidsForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.customer_id = request.user
            bid.item_id = Item.objects.filter(id=pk).first()
            bid.time = datetime.now()
            bid.save()
            return redirect(reverse('auction:customer_bids'))
        else:
            return render(request, 'Customer_BidAgain.html', {'item': item, 'form': form, 'mycurrentBid': mycurrentBid})
    else:
        form = CustomerBidsForm()
        return render(request, 'Customer_BidAgain.html', {'item': item, 'form': form, 'mycurrentBid': mycurrentBid})

# method to delete bids
@login_required()
def customerBidDelete(request, pk):
    bid = Bid.objects.filter(id=pk).first()
    if request.user.id != bid.customer_id.id:
        return HttpResponseForbidden()
    bid.delete()
    bids = Bid.objects.filter(customer_id=request.user).order_by('-time')
    return render(request, 'Customer_Bidslist.html', {'bids': bids})

# making pdf for the history of bids done on the customer owned items
def sendpdfEmail(request):
    bids = Bid.objects.filter(item_id__customer_id=request.user).order_by('-time')
    myItems = Item.objects.filter(customer_id=request.user)
    context = {'bids':bids, 'myItems':myItems}
    pdfbytes = render_to_pdf('Customer_ItemBidlistPDF.html', context)
    sendEmail(pdfbytes,request)
    return render(request, 'Customer_Itemslist.html', {'items': myItems})

# method to make pdf
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.replace(u'\ufeff', '').encode("latin-1")), result)
    if not pdf.err:
        return result.getvalue()
    return None

# method to send email of the pdf
def sendEmail(pdf,request):
    username = request.user
    email= request.user.email
    subject = "JustBid - Request for MyItems-Bid History Report "
    content = {'uname': username, 'jb_site_name': 'Just Bid.com'}
    from_email = settings.EMAIL_HOST_USER
    to_email = email
    message = EmailMultiAlternatives(subject=subject, body="Welcome..", from_email=from_email,
                                     to=[to_email], )
    html_template = get_template("customer_email_generation_myitems-bids.html").render(context=content)
    message.attach_alternative(html_template, "text/html")
    message.attach('MyItems-BidHistory.pdf', pdf, 'application/pdf')
    print("message send status=",message.send())




