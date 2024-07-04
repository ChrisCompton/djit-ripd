from django.shortcuts import render

def index(request, item):
    context = {
        'item': item
    }
    return render(request, 'index.html', context)

def read(request, item, id):
    context = {
        'item': item,
        'id': id
    }
    return render(request, 'read.html', context)

def insert(request, item):
    context = {
        'item': item
    }
    return render(request, 'insert.html', context)

def patch(request, item, id):
    context = {
        'item': item,
        'id': id
    }
    return render(request, 'patch.html', context)

def put(request, item, id):
    context = {
        'item': item,
        'id': id
    }
    return render(request, 'put.html', context)

def delete(request, item, id):
    context = {
        'item': item,
        'id': id
    }
    return render(request, 'delete.html', context)