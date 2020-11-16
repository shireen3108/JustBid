# this tags are purely to use django built in functions in template - Apr 9 2020
from datetime import datetime, timedelta
from django.template.defaultfilters import stringfilter
from django.utils import timezone

from django import template

from auction.models import Bid

register = template.Library()


@register.filter(name='maxBidValue')
def maxBidValue(item_id):
    maxBid = Bid.objects.filter(item_id=item_id).order_by('-time').first()
    if maxBid is None:
        return False
    else:
        return maxBid.amount


@register.filter(name='maxBidBy')
def maxBidBy(item_id):
    maxBid = Bid.objects.filter(item_id=item_id).order_by('-time').first()
    return maxBid.customer_id.username

@register.filter(name='maxBidById')
def maxBidById(item_id):
    maxBid = Bid.objects.filter(item_id=item_id).order_by('-time').first()
    return maxBid.id


@register.filter(name='getBidsCount')
def getBidsCount(item_id):
    bids = Bid.objects.filter(item_id=item_id)
    return bids.count()

@register.filter(name='getMyBidsCount')
def getMyBidsCount(item_id,user):
    bids = Bid.objects.filter(item_id=item_id,customer_id=user.id)
    return bids.count()


@register.filter(is_safe=False)
@stringfilter
def endswith(value, suffix):
    return value.endswith(suffix)


@register.filter(name='checkEndDatePassed')
def checkEndDatePassed(enddate):
    now = datetime.today()
    print('enddate bef', enddate)
    enddate = enddate.replace(tzinfo=None)- timedelta(hours=6)
    print('now', now)
    print('enddate', enddate)
    if enddate > now:
        return True
    else:
        return False


