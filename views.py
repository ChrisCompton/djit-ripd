from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Item
from .forms import ItemForm

def all_in_one(request, item_name, id=None):
    """Manage all CRUD operations in a single view."""
    context = {
        'item_name': item_name,
        'id': id
    }

    form = ItemForm()

    if id is not None:
        if request.method == 'DELETE':
            print("Handling Record DELETE request")
            basic_delete(request, item_name, id)

        elif request.method == 'PATCH':
            print("Handling Record PATCH request")
            basic_patch(request, item_name, id)

        elif request.method == 'PUT':
            print("Handling Record PUT request")
            item = get_object_or_404(Item, pk=id)
            context['item'] = item

            form = ItemForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
                context['success'] = 'Item created successfully.'
            else:
                context['error'] = 'Error creating item.'

        elif request.method == 'POST':
            print("Handling Record POST request")
            item = get_object_or_404(Item, pk=id)
            context['item'] = item

            form = ItemForm(instance=item)

        elif request.method == 'GET':
            print("Handling Record GET request")
            item = get_object_or_404(Item, pk=id)
            context['item'] = item

            form = ItemForm(instance=item)
    else:
        if request.method == 'POST':
            print("Handling New POST request")
            form = ItemForm(request.POST)
            
            if form.is_valid():
                form.save()
                context['success'] = 'Item created successfully.'
            else:
                context['error'] = 'Error creating item.'
                print(form.errors.as_json())
        else:
            print("Handling Default request", request.method)
            form = ItemForm()
    
    context['form'] = form

    items = Item.objects.all()
    context['items'] = items

    print("Context",context)

    render_template = 'all_in_one/index.html'
    return render(request, render_template, context)



def basic_list(request, item):
    context = {
        'item': item
    }

    items = Item.objects.all()
    """Get all items."""

    context['items'] = items

    return render(request, 'basic/list.html', context)

def basic_read(request, item, id):
    """Read a single item."""

    context = {
        'item': item,
        'id': id
    }

    item = Item.objects.get(id=id)
    context['item'] = item

    return render(request, 'basic/read.html', context)

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

    form = ItemForm()
    context['form'] = form

    return render(request, 'basic/insert.html', context)


@csrf_exempt
def basic_patch(request, item, id):
    """Patch an existing item."""
    if request.method == 'POST':
        # Retrieve the item, or return a 404 if not found
        item = get_object_or_404(Item, id=id)

        # Update fields if provided in the request
        name = request.POST.get('name', None)
        description = request.POST.get('description', None)
        classification = request.POST.get('classification', None)

        if name is not None:
            item.name = name
        if description is not None:
            item.description = description
        if classification is not None:
            item.classification = classification

        # Save the item to apply changes
        item.save()

        # Return a success response
        return JsonResponse({'success': 'Item updated successfully.'}, status=200)
    else:
        # Return an error response if the request method is not POST
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

def basic_put(request, item, id):
    """Put an existing item."""

    context = {
        'item': item,
        'id': id
    }

    item = Item.objects.get(id=id)
    #update item where values changed:
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        classification = request.POST.get('classification')

        item.name = name
        item.description = description
        item.classification = classification
        result = item.save()

        ## If successful, return success message on context, if not, send error message
        if result:
            context['success'] = 'Item updated successfully.'
        else:
            context['error'] = 'Error updating item.'

    return render(request, 'basic/put.html', context)

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

    return render(request, 'basic/delete.html', context)