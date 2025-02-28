from django.urls import path
from .views import *
app_name='myapp'

urlpatterns=[
    path('',homepage,name='homepage'),
    path('cartpage/',cartPage,name='cartpage'),
    path('orders/',orders,name='orders'),
    #path('login/',login,name='login'),
    #path('signup/',signup,name='signup'),
    # path('milkshakes/',milkshakes,name='milkshakes'),
    # path('fruitjuices/',fruitjuices,name='fruitjuices'),
    # path('hotbeverages/',hotbeverages,name='hotbeverages'),
    # path('softdrinks/',softdrinks,name='softdrinks'),
    # path('energydrinks/',energydrinks,name='energydrinks'),
    # path('mocktails/',mocktails,name='mocktails'),
    # path('beers/',beers,name='beers'),
    # path('wines/',wines,name='wines'),
    path('category/<int:category_id>/', category_view, name='category_view'),
    path('addtocart/<int:id>',addToCart,name='addtocart'),
    path('update_cart',update_cart,name='update_cart'),
    path('delete_item',delete_item,name='delete_item'),
    path('place_order/', place_order, name='place_order'),
    path('offer_milk/<int:d>/', offer_milk, name='offer_milk'),
    path('owner/', owner_login, name='owner_login'),
    #path('logout/', logout_owner, name='logout_owner'),
    path('ownerhome/', owner_home, name='owner_home'),
    path('logout_owner/', logout_owner, name='logout_owner'),
    # Categories CRUD
    path('categories/', show_categories, name='show_categories'),
    path('categories/add/', add_category, name='add_category'),
    path('categories/edit/<int:id>/', edit_category, name='edit_category'),
    path('categories/delete/<int:id>/', delete_category, name='delete_category'),

    # Products CRUD
    path('products/', show_products, name='show_products'),
    path('products/add/', add_product, name='add_product'),
    path('products/edit/<int:id>/', edit_product, name='edit_product'),
    path('products/delete/<int:id>/', delete_product, name='delete_product'),

]