from django.contrib import admin

from .models import (
    BlogCategory,
    BlogComment,
    BlogPost,
    ForumCategory,
    ForumPost,
    ForumTopic,
    Order,
    Product,
    ProductCategory,
    Profile,
)

admin.site.register(Profile)
admin.site.register(BlogCategory)
admin.site.register(BlogPost)
admin.site.register(BlogComment)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(ForumCategory)
admin.site.register(ForumTopic)
admin.site.register(ForumPost)
