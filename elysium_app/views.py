# from django.http import JsonResponse
# from django.shortcuts import render
# from elysium_app.models import Stock

# # Create your views here.
# def portfolio(request):
#     stocks = Stock.objects.all()
#     data={
#         'stocks':list(stocks.values())
#     }
#     return JsonResponse(data)

# def portfolio_details(request,pk):
#     stocks=Stock.objects.get(pk=pk)
#     data={
#         'name': stocks.name,
#         'Bought For': stocks.boughtFor, 
#         'Hold': stocks.hold
#     }
#     return JsonResponse(data)