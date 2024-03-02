from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from checkout.forms import OrderForm
from owner.models import PostageSettings, Voucher

# Create your views here.
class CheckoutView(generic.ListView):
    
    template_name = "checkout/checkout.html"
    
    def get(self, request, *args, **kwargs):
        # Starting points
        postage_settings = PostageSettings.objects.filter(pk=1).first()
        order_form = OrderForm()
        subtotal = request.session.get('subtotal', 0)
        standard_delivery_cost = round((float(postage_settings.standard_delivery) * subtotal / 100), 2)
        express_delivery_cost = round((float(postage_settings.express_delivery) * subtotal / 100), 2)
        total = subtotal + standard_delivery_cost
        voucher_used = False
        # If User is logged in
        if request.user.is_authenticated:
            order_form = OrderForm(instance=request.user)
        return render(
            request,
            self.template_name,
            {
                "order_form": order_form,
                "standard_delivery_cost": standard_delivery_cost,
                "express_delivery_cost": express_delivery_cost,
                "voucher_used": voucher_used,
                "total": total,
            }
        )
        
    def post(self, request, *args, **kwargs):
        """
        Voucher in use : voucher_used, voucher_code, discount_applied, voucher_discount
        """
        postage_settings = PostageSettings.objects.filter(pk=1).first()
        order_form = OrderForm(request.POST)
        subtotal = request.session.get('subtotal', 0)
        # Delivery starting points
        standard_delivery_cost = round((float(postage_settings.standard_delivery) * subtotal / 100), 2)
        express_delivery_cost = round((float(postage_settings.express_delivery) * subtotal / 100), 2)
        selected_delivery = request.session.get('selected_delivery', 0)
        print(selected_delivery)
        # Vouchers starting points
        current_voucher = request.session.get('current_voucher', [False, '', 0, 0])
        if 'delivery' in request.POST:
            if request.POST.get('delivery_option') == '1':
                selected_delivery_cost = express_delivery_cost
                request.session['selected_delivery'] = '1'
            else:
                selected_delivery_cost = standard_delivery_cost
                request.session['selected_delivery'] = '0'
            
        if 'check-voucher' in request.POST:
            voucher_code = request.POST.get('voucher','')
            if voucher_code != '':
                usable_voucher = Voucher.objects.filter(voucher_code__contains=voucher_code).first()
                if usable_voucher:
                    current_voucher[1] = usable_voucher.voucher_code
                    if usable_voucher.status == 'Active':
                        current_voucher[0] = True
                        current_voucher[2] = round((subtotal * usable_voucher.discount / 100), 2)
                        current_voucher[3] = usable_voucher.discount
                        subtotal = subtotal - current_voucher[2]
                        messages.success(request, f'Code {usable_voucher.voucher_code} valid. You gained {usable_voucher.discount} % discount.')
                    else:
                        messages.error(request, f"Voucher Code {voucher_code} is not active.")
                        order_form = OrderForm(initial={'voucher': ''})
                else:
                    messages.error(request, f"Voucher Code {voucher_code} is not valid.")
                    order_form = OrderForm(initial={'voucher': ''})
            else:
                messages.error(request, "Voucher Code can't be empty.")
                order_form = OrderForm(initial={'voucher': ''})
        request.session['current_voucher'] = current_voucher
        if 'delete-voucher' in request.POST:
            current_voucher = [False, '', 0, 0]
            messages.success(request, 'Voucher removed.')
        total = round((subtotal + selected_delivery_cost - current_voucher[2]), 2)
        return render(
            request,
            self.template_name,
            {
                "order_form": order_form,
                "standard_delivery_cost": standard_delivery_cost,
                "express_delivery_cost": express_delivery_cost,
                "current_voucher": current_voucher,
                "total": total,
                "selected_delivery_cost": selected_delivery_cost,
            }
        )