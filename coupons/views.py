from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from coupons.models import Coupon
from coupons.forms import CouponApplyForm
from utils.constants import KEY_COUPON_ID
from carts.carts import Cart
# Create your views here.


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session[KEY_COUPON_ID] = coupon.id
        except Coupon.DoesNotExist:
            request.session[KEY_COUPON_ID] = None

    return redirect('carts:cart_detail')

