import datetime
from orders.models import (SpecificationType, Particular, ParticularSpecificationTypePricing,
                           OrderPayment)


def get_order_estimate(data):
    particulars = data['particulars']
    base_price = 0
    spec_price = 0
    for particular in particulars.validated_data:
        base_price += particular['particular'].base_price
        for specification in particular['specifications'].validated_data:
            if specification['specification_type']:
                specification_price = ParticularSpecificationTypePricing.objects.filter(
                    particular_id=particular['particular'],
                    specification_type=specification['specification_type']
                ).first()
            else:
                specification_price = ParticularSpecificationTypePricing.objects.filter(
                    particular=particular['particular'],
                    specification_type__specification=specification['specification']
                ).order_by('-price').first()
            if specification_price:
                specification_price = specification_price.price
            else:
                specification_price = 100
            spec_price += specification_price

    price = base_price + spec_price + round(base_price * 0.6)
    return price


def handle_order_payment(data):
    event = data['event']
    invoice_id = data['payload'].get('payment', {}).get('entity', {}). get('invoice_id')
    if event == 'payment.authorized':
        try:
            order_payment = OrderPayment.objects.get(razorpay_invoice_id=invoice_id, is_paid=False)
            order_payment.is_paid = True
            order_payment.paid_at = datetime.datetime.now()
            order_payment.order.amount_paid += order_payment.amount
            order_payment.save()
            order_payment.order.save()
        except OrderPayment.DoesNotExist:
            pass
