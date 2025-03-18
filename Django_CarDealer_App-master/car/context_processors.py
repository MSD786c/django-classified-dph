# This file is needed for  passing variable to base.html
from .models import Car, Privacy, Ads


def ad_processor(request):
    popup_ad = Ads.objects.all()
    if popup_ad.exists():  # Check if there are any ads
        return {
            'ad': popup_ad[0]
        }
    else:
        return {
            'ad': None  # Return None or a default value if no ads are found
        }