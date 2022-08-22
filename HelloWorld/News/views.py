from django.http import HttpResponse
import akshare as ak


def top4(request):
    df = ak.stock_telegraph_cls()
    i=0
    while i==4:
        if df.iat[0,'标题']!="":
            df.drop(i)
        else:
            i+=1
    df=df.loc[0:3,'标题']

    return HttpResponse(df.to_json())
