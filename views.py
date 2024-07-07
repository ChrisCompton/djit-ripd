from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from .models import Item
from .forms import ItemForm





def htmx_handler(request, item_name, id=None):
    """Manage all CRUD operations in a single view."""
    context = {
        'item_name': item_name,
        'id': id
    }
    render_template = 'index.html'

    form = ItemForm()

    if id is not None:
        if request.method == 'DELETE':
            print("Handling Record DELETE request")
            basic_delete(request, item_name, id)

        elif request.method in ['PATCH','PUT','POST']:
            print("Handling Record POST UPDATE request")
            basic_update(request, item_name, id)

        elif request.method == 'GET':
            print("Handling Record GET request")
            item = get_object_or_404(Item, pk=id)
            context['item'] = item

            form = ItemForm(instance=item)
    else:
        if request.method == 'POST':
            print("Handling New POST request")
            basic_insert(request, item_name)
        else:
            print("Handling Default request", request.method)
            form = ItemForm()
    
    context['form'] = form

    items = Item.objects.all()
    context['items'] = items

    print("Context",context)

    response = render(request, render_template, context)

    response['HX-Trigger'] = 'refreshTasks'
    return response



def list_items(request, item_name):
    items = Item.objects.all()
    context = {
        'item_name': item_name,
        'items': items
    }

    html = render_to_string('partials/list_items.html', context, request)
    response = HttpResponse(html)

    return response







def basic_insert(request, item):
    """Insert a new item."""

    context = {
        'item': item
    }

    ### Insert into database
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            context['success'] = 'Item created successfully.'
        else:
            context['error'] = 'Error creating item.'

    html = render_to_string('partials/list_items.html', context, request)
    response = HttpResponse(html)

    response['HX-Trigger'] = 'refreshTasks'
    return response


def basic_update(request, item, id):
    """Put an existing item."""

    context = {
        'item': item,
        'id': id
    }

    item = Item.objects.get(id=id)
    #update item where values changed:
    if request.method == 'POST':
        form = ItemForm(request.POST)

        if form.is_valid():
            item.name = form.cleaned_data["name"]
            item.description = form.cleaned_data["description"]
            result = item.save()

            ## If successful, return success message on context, if not, send error message
            if result:
                context['success'] = 'Item updated successfully.'
            else:
                context['error'] = 'Error updating item.'
        else:
            print("ERROR: Form is not valid")
            context['error'] = 'The form is not valid.'

    html = render_to_string('partials/list_items.html', context, request)
    response = HttpResponse(html)

    response['HX-Trigger'] = 'refreshTasks'
    return response


def basic_delete(request, item, id):
    """Delete an existing item."""

    context = {
        'item': item,
        'id': id
    }

    item = Item.objects.get(id=id)
    result = item.delete()

    ## If successful, return success message on context, if not, send error message
    if result:
        context['success'] = 'Item deleted successfully.'
    else:
        context['error'] = 'Error deleting item.'

    html = render_to_string('partials/list_items.html', context, request)

    response = HttpResponse(html)

    response['HX-Trigger'] = 'refreshTasks'
    return response