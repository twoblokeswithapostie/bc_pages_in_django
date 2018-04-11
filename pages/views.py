import pdb

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from bcapps.models import Site
from .api import PageClient, GetException, PutException
from .forms import PageForm
from .models import Page


@login_required
def index(request):
    pages = Page.objects.all().order_by('name')
    return render(request, 'pages/index.html', {'pages': pages})


@login_required
def detail(request, page_id):
    page = get_object_or_404(Page, pk=page_id)
    form = PageForm(instance=page)
    if request.method == 'POST':
        form = PageForm(data=request.POST, instance=page)
        if form.is_valid():
            site = Site.objects.get(site_id=request.site_id)
            client = PageClient(site)
            try:
                resp = client.update_page(page)
            except (GetException, PutException) as e:
                messages.error(request, "%s" % e)
            else:
                if resp.status_code == 200 or resp.status_code == 204:
                    form.save()
                    messages.success(request, 'Form saved.')
                    return redirect('pages:index')
                else:
                    messages.error(request, 'There was a problem with website. '
                                            'Code: %s. Message: %s' % (resp.status_code, resp.text))
        else:
            messages.error(request, 'Form invalid. Please fix the errors and try again.')
    return render(request, 'pages/detail.html', {'page': page, 'form': form})


@login_required
def update_pages(request):
    site = Site.objects.get(site_id=request.site_id)
    client = PageClient(site)
    try:
        client.get_all_items()
        messages.success(request, 'Pages Updated')
    except (GetException, PutException) as e:
        messages.error(request, "%s" % e)
    return redirect('pages:index')
