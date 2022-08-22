from django.http import HttpResponse
import akshare as ak


def top4(request):
    stock_telegraph_cls_df = ak.stock_telegraph_cls()
    df=stock_telegraph_cls_df.loc[0:3,'标题']
    print(df)
    return HttpResponse(df.to_json())
