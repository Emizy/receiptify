import uuid
from io import BytesIO

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.crypto import get_random_string
from django_xhtml2pdf.utils import generate_pdf, render_to_pdf_response
from xhtml2pdf import pisa
from apps.core.models import Order, OrderItem, ReceiptHistory


class Addon:
    """
    class method that handle the utility method of the system
    """

    def __init__(self):
        super().__init__()

    def generate_uuid(self, model, column):
        """
        method handle generate unique uuid based on the model and colume supplied
        """
        unique = str(uuid.uuid4())
        kwargs = {column: unique}
        qs_exists = model.objects.filter(**kwargs).exists()
        if qs_exists:
            return self.generate_uuid(model, column)
        return unique

    def unique_number_generator(self, model, field, length=6, allowed_chars="0123456789"):
        """
        method handle generating of unique number based on the supplied model and field
        :param model:
        :param field:
        :param length:
        :param allowed_chars:
        """
        unique = get_random_string(length=length, allowed_chars=allowed_chars)
        kwargs = {field: unique}
        qs_exists = model.objects.filter(**kwargs).exists()
        if qs_exists:
            return self.unique_number_generator(model, field, length)
        return unique

    @staticmethod
    def generate_order_pdf(order_id, number_of_pdf=10):
        """
        method handles generating pdf for an order
        :param: order
        :param: number_of_pdf
        """
        context = {}
        try:
            order = Order.objects.filter(id=order_id).first()
            order_item = OrderItem.objects.filter(order=order)
            total_amount_payable = OrderItem.objects.filter(order=order).aggregate(total=Sum('price'))
            result = render_to_pdf_response('receipt/receipt.html', context={'order': order, 'order_items': order_item,
                                                                             'total_amount_payable': total_amount_payable.get(
                                                                                 'total', 0.0)})
            receipt_file = BytesIO(result.content)
            if result.status_code == 200:
                for num in range(number_of_pdf):
                    history = ReceiptHistory()
                    history.order = order
                    history.pdf = File(receipt_file, str(f'invoice_{order_id}_{order.customer.name}_{num + 1}.pdf'))
                    history.save()
            context.update({'result': result})
        except Exception as ex:
            context.update({'message': str(ex)})
        return context
