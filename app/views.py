from django.shortcuts import render, redirect
from app.models import DogProduct, DogTag, Purchase
from app.forms import NewDogTagForm
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime


def home(request):
    dog_products = DogProduct.objects.all()
    return render(request, "home.html", {"dog_products": dog_products})


def dog_product_detail(request, dog_product_id):
    dog_product = DogProduct.objects.get(id=dog_product_id)
    return render(request, "dog_product_detail.html", {"dog_prduct": dog_product})


def purchase_dog_product(request, dog_product_id):
    dog_product = DogProduct.objects.get(id=dog_product_id)
    if dog_product_id.in_stock:
        DogProduct.quantity - 1
        purchase = dog_product.purchase_set.create(datetime=datetime)
        messages.success(request, f"Purchase {DogProduct.name}")
        return redirect("purchase_detail")
    else:
        messages.error(request, f"{DogProduct.name} is out of stock")
        return redirect("purchase_detail")


def purchase_detail(request, purchase_id):
    purchase = Purchase.objects.get(id=purchase_id)
    return render(request, "purchase_detail.html", {"purchase": purchase})


def new_dog_tag(request):
    if request.method == "GET":
        return render(request, "new_dog_tag.html")
    else:
        form = NewDogTagForm(request.POST)
        if form.is_valid():
            dog_tag = DogTag.objects.create(
                owner_name=form.cleaned_data["owner_name"],
                dog_name=form.cleaned_data["dog_name"],
                dog_birthday=form.cleaned_data["dog_birthday"],
            )
            return redirect("dog_tag_list")
        else:
            return render(request, "new_dog_tag.html", {"form": NewDogTagForm()})


def dog_tag_list(request):
    dog_tags = DogTag.objects.all()
    return render(request, "dog_tag_list.html", {"dog_tags": dog_tags})

