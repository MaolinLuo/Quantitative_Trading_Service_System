import json

from django.http import HttpResponse
import akshare as ak


def top4(request):
    df = ak.stock_telegraph_cls()
    df = df.loc[0:3, '标题']
    return HttpResponse(df.to_json())
