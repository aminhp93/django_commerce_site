
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import stripe

 
stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
@login_required
def checkout(request):
	publishKey = settings.STRIPE_PUBLISHABLE_KEY
	print request.user.userstripe.stripe_id
	customer_id = request.user.userstripe.stripe_id
	if request.method == 'POST':
		print request.POST
		token = request.POST['stripeToken']
		print token

		try:
			customer = stripe.Customer.retrieve(customer_id)
			customer.sources.create(source=token)
		 	charge = stripe.Charge.create(
		      amount=1000, # Amount in cents
		      currency="usd",
		      # source=token,
		      customer = customer,
		      description="Example charge"
		  	)
		except stripe.error.CardError as e:
		  # The card has been declined
		  pass
	context = {'publishKey': publishKey}
	template = 'checkout.html'
	return render(request, template, context)