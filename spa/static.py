from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from dss import settings


def get_events(request):
    # What you want the button to do.
    paypal_dict = {
        "business": "admin@deepsouthsounds.com",
        "amount": "0.01",
        "item_name": "DSS Love Bites",
        "invoice": "unique-invoice-id",
        "notify_url": settings.PAYPAL_NOTIFY_URL,
        "return_url": settings.PAYPAL_RETURN_URL,
        "cancel_return": settings.PAYPAL_CANCEL_URL,
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}

    return render(
        request,
        'inc/bitsnbobs/moodymanc.html',
        content_type='text/html; charset=utf-8'
    )