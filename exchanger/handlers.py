from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

PAGINATOR_QTY = 10


def get_paginator(request, data_list):
    paginator = Paginator(data_list, per_page=PAGINATOR_QTY)
    page_numer = request.GET.get('page', 1)
    page_range = []
    if len(data_list) > PAGINATOR_QTY:
        page_range = paginator.get_elided_page_range(number=paginator.num_pages // 2, on_each_side=3, on_ends=2)

    try:
        data_ = paginator.page(page_numer)
    except PageNotAnInteger:
        data_ = paginator.page(1)
    except EmptyPage:
        data_ = paginator.page(paginator.num_pages)

    return data_, page_range
