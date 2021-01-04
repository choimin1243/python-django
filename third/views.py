from django.shortcuts import render,get_object_or_404,redirect
from third.models import Restaurant,Review
# Create your views here.
from django.core.paginator import Paginator
from third.forms import RestaurantForm, ReviewForm ,UpdateRestaurantForm
from django.http import HttpResponseRedirect
from django.db.models import Count, Avg



def list(request):
    restaurants= Restaurant.objects.all().annotate(reviews_count=Count('review')).annotate(average_point=Avg('review__point'))
    paginator=Paginator(restaurants,5)
    page=request.GET.get('page')
    items=paginator.get_page(page)
    context={
        'restaurant': items
    }
    return render(request,'third/list.html',context)

def create(request):
    if request.method=='POST':
        form=RestaurantForm(request.POST)
        if form.is_valid():
            new_item=form.save()

        return HttpResponseRedirect('../list/')


    form=RestaurantForm()
    return render(request,'third/create.html',{'form': form})

def update(request):
    if request.method == 'POST' and 'id' in request.POST:
        item=get_object_or_404(Restaurant,pk=request.POST.get('id'))
        password=request.POST.get('password','')
        form = UpdateRestaurantForm(request.POST, instance=item)  # NOTE: instance 인자(수정대상) 지정
        if form.is_valid() and password==item.password:
            item = form.save()
    if 'id' in request.GET:
        item = Restaurant.objects.get(pk=request.GET.get('id'))
        form = RestaurantForm(instance=item)
        return render(request, 'third/update.html', {'form': form})

    return HttpResponseRedirect('/third/list/')

def detail(request,id):
    if id is not None:
        item=get_object_or_404(Restaurant,pk=id)
        reviews=Review.objects.filter(restaurant=item).all()
        return render(request,'third/detail.html',{'item': item,'reviews':reviews})
    return HttpResponseRedirect('/third/list/')


def delete(request, id):
    item = get_object_or_404(Restaurant, pk=id)
    if request.method == 'POST' and 'password' in request.POST or item.password is None:
        if item.password == request.POST.get('password'):
            item.delete()
            return redirect('list')  # 리스트 화면으로 이동합니다.

        return redirect('restaurant-detail', id=id)  # 비밀번호가 입력되지 않으면 상세페이지로 되돌아감

    return render(request, 'third/delete.html', {'item': item})


def review_create(request, restaurant_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)  #
        if form.is_valid():  # 데이터가 form 클래스에서 정의한 조건 (max_length 등)을 만족하는지 체크합니다.
            new_item = form.save()  # save 메소드로 입력받은 데이터를 레코드로 추가합니다.
        return redirect('restaurant-detail', id=restaurant_id)  # 전화면으로 이동합니다.

    item = get_object_or_404(Restaurant, pk=restaurant_id)
    form = ReviewForm(initial={'restaurant': item})
    return render(request, 'third/review_create.html', {'form': form, 'item':item})

def review_delete(request,restaurant_id,review_id):
    item=get_object_or_404(Review,pk=review_id)
    item.delete()
    return redirect('restaurant-detail',id=restaurant_id)

def review_list(request):
    reviews=Review.objects.all().select_related().order_by('-created_at')
    paginator=Paginator(reviews,10)
    page=request.GET.get('page')
    items=paginator.get_page(page)

    context={
        'reviews':items
    }

    return render(request, 'third/review_list.html',context)



