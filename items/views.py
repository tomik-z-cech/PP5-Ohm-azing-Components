# Imports
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Count, F, ExpressionWrapper, fields, Q
from django.core.paginator import Paginator
from items.models import Category, Item


class ShopView(generic.ListView):
    """
    Class generates view of items page
    """

    template_name = "items/shop.html"

    def get(self, request, category_pk, *args, **kwargs):
        """This method generates view of items page"""
        all_categories = Category.objects.all().order_by('category_name')
        page_sort = int(request.GET.get('page_sort', 0))
        page_length = int(request.GET.get('page_length', 8))
        current_page = request.GET.get('page', 1)
        if category_pk == 0:
            queryset = Item.objects.all().order_by('item_name').annotate(
            like=Count("item_likes"),
            dislike=Count("item_dislikes"),
            item_likes_num=ExpressionWrapper(
                F('like') - F('dislike'),
                output_field=fields.IntegerField()
                )
            ).annotate(
            item_comments_num=Count(
                "item_comments", filter=Q(item_comments__approved=1)
            )
        )
            selected_category = 'All Products'
        else:
            queryset = Item.objects.filter(item_category__pk=category_pk).annotate(
            like=Count("item_likes"),
            dislike=Count("item_dislikes"),
            item_likes_num=ExpressionWrapper(
                F('like') - F('dislike'),
                output_field=fields.IntegerField()
                )
            ).annotate(
            item_comments_num=Count(
                "item_comments", filter=Q(item_comments__approved=1)
            )
        )
            running_category = Category.objects.filter(pk=category_pk).first()
            selected_category = running_category.category_name
        if page_length != 0:
            if page_sort == 5:
                paginated_items = Paginator(queryset.order_by('item_likes_num'), page_length)
            elif page_sort == 4:
                paginated_items = Paginator(queryset.order_by('-item_likes_num'), page_length)
            elif page_sort == 3:
                paginated_items = Paginator(queryset.order_by('-price_per_unit'), page_length)
            elif page_sort == 2:
                paginated_items = Paginator(queryset.order_by('price_per_unit'), page_length)
            elif page_sort == 1:
                paginated_items = Paginator(queryset.order_by('-item_name'), page_length)
            elif page_sort == 0:
                paginated_items = Paginator(queryset.order_by('item_name'), page_length)
            else:
                paginated_items = Paginator(Item.objects.all(), 10)
            page_obj = paginated_items.get_page(current_page)
            paginator_nav = True
        else:
            if page_sort == 5:
                page_obj = queryset.order_by('item_likes_num')
            elif page_sort == 4:
                page_obj = queryset.order_by('-item_likes_num')
            elif page_sort == 3:
                page_obj = queryset.order_by('-price_per_unit')
            elif page_sort == 2:
                page_obj = queryset.order_by('price_per_unit')
            elif page_sort == 1:
                page_obj = queryset.order_by('-item_name')
            elif page_sort == 0:
                page_obj = queryset.order_by('item_name')
            else:
                page_obj = Item.objects.all()
            paginator_nav = False
        # Render template
        return render(
            request,
            self.template_name,
            {
                "all_categories": all_categories,
                "items": page_obj,
                "selected_category": selected_category,
                "paginator_nav": paginator_nav,
                "page_sort": page_sort,
                "page_length":page_length,
            },
        )
        
        
class ItemDetailView(generic.ListView):
    """
    Class generates view of item's detail
    """

    template_name = "items/item_detail.html"
    
    def get(self, request, item_pk, *args, **kwargs):
        item_to_view = get_object_or_404(Item, pk=item_pk)
        # Render template
        return render(
            request,
            self.template_name,
            {
                "item": item_to_view,
            },
        )