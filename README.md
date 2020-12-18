# eShop
An online shop to let customers purchase items at the comfort of sitting in their homes.
A Customer can visit the shop and check multiple products belongs to different categories.

User can add multiple items a cart and proceed to checkout. A payment gateway is integrate to allow users to 
pay at the time of checkout.

This site is internationalized into two languages ``English``and `Espanish`.
Localized versions are available via URL language prefix and localized URLs.

This project uses ``Django-parlor``for model fields locations and `django-localflavor`
for country specific validation fields.

A simple recommendation system is also in place to recommend the user frequently bought together items using `redis`.