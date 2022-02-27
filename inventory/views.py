from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from inventory.forms import CheckInForm, CheckOutForm, OrderForm

from inventory.models import InstoreItem, OnHandItem, OrderByEmployee

def check_out(request, pk):
    selected_instore_item = InstoreItem.objects.get(pk=pk)
    if request.method == 'POST':
        form = CheckOutForm(request.POST)
        if form.is_valid():

            if selected_instore_item.quantity < form.cleaned_data['quantity']:
                return render(request, 'checkout.html', {
                    'form': form,
                    'pk': pk,
                    'message': 'You are specifing more than there is in store'
                })


            selected_instore_item.quantity -= form.cleaned_data['quantity']


            OnHandItem.objects.create(
                name=selected_instore_item.name,
                model=selected_instore_item.model,
                serie=selected_instore_item.serie,
                quantity=form.cleaned_data['quantity'],
                employee=form.cleaned_data['employee'],
            ).save()

            if selected_instore_item.quantity == 0:
                selected_instore_item.delete()
            else:
                selected_instore_item.save()

            return HttpResponseRedirect('/admin/inventory/instoreitem/')

    else:
        form = CheckOutForm({
            "quantity": selected_instore_item.quantity,
        })

    return render(request, 'checkout.html', {'form':form, 'pk': pk})

def check_in(request, pk):
    returned_item = OnHandItem.objects.get(pk=pk)
    if request.method == 'POST':
        form = CheckInForm(request.POST)
        if form.is_valid():
            if returned_item.quantity < form.cleaned_data['quantity']:
                return render(request, 'checkout.html', {
                    'form': form,
                    'pk': pk,
                    'message': 'You are specifing more than there is in store'
                })

            ret_instore = InstoreItem.objects.filter(
                name=returned_item.name,
                model=returned_item.model,
                serie=returned_item.serie,
            )

            if len(ret_instore) == 0:
                InstoreItem.objects.create(
                    name=returned_item.name,
                    model=returned_item.model,
                    serie=returned_item.serie,
                    quantity=form.cleaned_data['quantity'],
                ).save()
            else:
                ret_instore = ret_instore.first()
                ret_instore.quantity += form.cleaned_data['quantity']
                ret_instore.save()

            returned_item.quantity -= form.cleaned_data['quantity']

            if returned_item.quantity == 0:
                returned_item.delete()
            else:
                returned_item.save()
            return HttpResponseRedirect('/admin/inventory/onhanditem/')
    else:
        form = CheckInForm({
            'quantity': returned_item.quantity,
        })
    return render(request, 'checkin.html', {'form': form, 'pk':pk})

def order_item(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            OrderByEmployee.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                ordered_by=form.cleaned_data['ordered_by'],
            ).save()
            return HttpResponseRedirect('/admin')

    else:
        form = OrderForm()

    return render(request, 'orderitem.html', {'form': form})

