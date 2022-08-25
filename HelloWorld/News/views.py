import json

from django.http import HttpResponse
import akshare as ak


def top4(request):
    df = ak.stock_telegraph_cls()
    # df = df.loc[0:3, '标题']
    res=[]
    i=0
    cnt=0
    while cnt!=4:
        if df.iat[i,0]!="":
            res.append(df.iat[i,0])
            cnt+=1
        i+=1
    return HttpResponse(json.dumps(res))
