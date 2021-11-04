
# coding: utf-8
# In[1]:
https://teams.microsoft.com/l/meetup-join/19%3ameeting_ZjE2Y2RmOTAtZGI2Zi00MGQ1LWFlMDUtMmQwNGFiNGUwNTFh%40thread.v2/0?context=%7b%22Tid%22%3a%220b9b90da-3fe1-457a-b340-f1b67e1024fb%22%2c%22Oid%22%3a%2232b669ba-f499-4cf4-8156-f7c35a413670%22%7d
https://teams.microsoft.com/dl/launcher/launcher.html?url=%2F_%23%2Fl%2Fmeetup-join%2F19%3Ameeting_M2ZmMDQxMzAtOTEwNS00N2NiLTk1ZDYtODllMWYxNGQxZTk4%40thread.v2%2F0%3Fcontext%3D%257b%2522Tid%2522%253a%252272f988bf-86f1-41af-91ab-2d7cd011db47%2522%252c%2522Oid%2522%253a%2522ed80446e-2f9b-44a7-a3ac-dcbbb4a519c3%2522%257d%26anon%3Dtrue&type=meetup-join&deeplinkId=6e1ce8f0-798d-49e9-9b78-b54c94da3e50&directDl=true&msLaunch=true&enableMobilePage=true&suppressPrompt=true
https://firstbank079.webex.com/firstbank079-tc/j.php?MTID=m94bcb88d8e278aba0c2df52d97d9db3b
###edited
##上市公司公司三大法人紀錄
import pandas as pd
import requests
import json
import datetime
from datetime import datetime as dt
from datetime import timedelta as td
import time
from random import randint
##產生日期序列
def daylist(n):
    daylist=(dt.now()- td(days=n)).strftime('%Y%m%d')
    return daylist

def InstitutionalInvestorsBS(dlist):
    time.sleep(randint(1, 5))
    url = "http://www.twse.com.tw/fund/T86?response=json&date={}&selectType=ALLBUT0999".format(dlist)
    res = requests.get(url)
    res.encoding='utf8'
    jd = json.loads(res.text)
    if jd['stat']=="OK":
        df = pd.DataFrame(jd['data'])
        if datetime.datetime.strptime(dlist, '%Y%m%d').strftime('%Y-%m-%d')>'2017-12-16':
            df1= df[[0,1,4,10,11]]
        else:df1= df[[0,1,4,7,8]]
        df1.columns=[u'證券代號', u'證券名稱',u'外陸買賣超',u'投信買賣超',u'自營買賣超']
        dict={
            u'證券代號':[(lambda x:str(df1.iloc[x,0]).strip())(x) for x in range(len(df1))],
            u'外陸買賣超':[(lambda x:int(''.join(str(df1.iloc[x,2]).split(','))))(x) for x in range(len(df1))],
            u'投信買賣超':[(lambda x:int(''.join(str(df1.iloc[x,3]).split(','))))(x) for x in range(len(df1))],
            u'自營買賣超':[(lambda x:int(''.join(str(df1.iloc[x,4]).split(','))))(x) for x in range(len(df1))]

        }
        arrays=[(lambda x:df1.iloc[x,1].strip())(x) for x in range(len(df1))]
        df2=pd.DataFrame(dict,columns=df1.columns[[0,2,3,4]],index=arrays)
        return df2
    else: return []
    
z0=InstitutionalInvestorsBS(daylist(1))
z1=InstitutionalInvestorsBS(daylist(2))


# In[2]:


z0[z0.iloc[:,1]>0]


# In[2]:


overbuy={u'外資':z0[u'外陸買賣超'].sort_values(ascending=False).head(10).index.tolist(), u'投信':z0[u'投信買賣超'].sort_values(ascending=False).head(10).index.tolist(), u'自營':z0[u'自營買賣超'].sort_values(ascending=False).head(10).index.tolist()}
oversell={u'外資':z0[u'外陸買賣超'].sort_values(ascending=False).tail(10).index.tolist(), u'投信':z0[u'投信買賣超'].sort_values(ascending=False).tail(10).index.tolist(), u'自營':z0[u'自營買賣超'].sort_values(ascending=False).tail(10).index.tolist()}

OverB=pd.DataFrame(overbuy)
OverS=pd.DataFrame(oversell)
a=set(OverB.iloc[:,0])&set(OverB.iloc[:,1])#取外資與投信買超聯集
#pd.DataFrame(list(a))[0]
print OverB
print OverS


# In[3]:


def GetConstantBS(n,day): #查詢法人連續買超個股
    nday=1
    listA=[]
    while len(listA)<day:
        z0=InstitutionalInvestorsBS(daylist(nday))
        print daylist(nday)
        if len(z0)>0:
            listA.append(z0)
            if len(listA)>1:
                new=listA[len(listA)-1].iloc[:,n]
                old=listA[len(listA)-2].iloc[:,n]
                #unionset=list(set()&set())
                if len(listA)<3:
                    unionset0=list((set(new[new>0].sort_values(ascending=False).index.tolist())& set(old[old>0].sort_values(ascending=False).index.tolist())))
                    
                else:
                    unionset0=list((set(new[new>0].sort_values(ascending=False).index.tolist())& set(unionset0)))
                    
            else:
                unionset0=z0.iloc[:,n].sort_values(ascending=False)

                
        nday=nday+1
    total=pd.DataFrame(unionset0)
    return total
ex=GetConstantBS(1,2)


# In[102]:


a=InstitutionalInvestorsBS(daylist(0))


# In[4]:


ex


# In[80]:


##上櫃公司公司三大法人紀錄
def InstitutionalInvestorsBStpex(dlist):
    time.sleep(randint(1, 5))
    url = "http://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php?l=zh-tw&se=EW&t=D&d={}/{}/{}".format(int(dlist[0:4])-1911,int(dlist[4:6]),int(dlist[6:8]))
    res = requests.get(url)
    res.encoding='utf8'
    jd = json.loads(res.text)
    if len(jd['aaData'])>0:
        df = pd.DataFrame(jd['aaData'])
        df1= df[[0,1,4,7,8]]
        df1.columns=[u'證券代號', u'證券名稱',u'外陸買賣超',u'投信買賣超',u'自營買賣超']
        dict={
            u'證券代號':[(lambda x:str(df1.iloc[x,0]).strip())(x) for x in range(len(df1))],
            u'外陸買賣超':[(lambda x:int(''.join(str(df1.iloc[x,2]).split(','))))(x) for x in range(len(df1))],
            u'投信買賣超':[(lambda x:int(''.join(str(df1.iloc[x,3]).split(','))))(x) for x in range(len(df1))],
            u'自營買賣超':[(lambda x:int(''.join(str(df1.iloc[x,4]).split(','))))(x) for x in range(len(df1))]

        }
        arrays=[(lambda x:df1.iloc[x,1].strip())(x) for x in range(len(df1))]
        tuples = list(zip(*arrays))
        df2=pd.DataFrame(dict,columns=df1.columns[2:5],index=arrays)
        return df2
    else: return []
InstitutionalInvestorsBStpex(daylist(1))


# In[1]:


import time
from random import randint
def CalPeriodBS(kind,period):
    first=InstitutionalInvestorsBS(daylist(1))
    record=list()
    record.append(first)
    indexA=list()
    indexA.append(first.index)

    for i in range(1,period):
        singleBS=InstitutionalInvestorsBS(daylist(i+1))
        print i
        if type(singleBS)==pd.core.frame.DataFrame:
            print daylist(i+1)
            record.append(singleBS)
            indexA.append(singleBS.index)
            #print len(indexA)
            Index_new1=set().union(*[indexA[-2],indexA[-1]])

    Vc=pd.DataFrame(index=Index_new1,columns=[u'外陸買賣超',u'投信買賣超',u'自營買賣超'])
    
    for j in range(len(record)):
        new=pd.DataFrame(record[j],index=Index_new1,columns=[u'外陸買賣超',u'投信買賣超',u'自營買賣超'])
        Vc=Vc.fillna(0)+new.fillna(0)
    return Vc
#a=Index_new  
b=CalPeriodBS(1,10)


# In[183]:


import numpy as np
left = pd.DataFrame({'A': ['A0', np.nan, 'A2', 'A3']},index=[1,2,3,4])
right = pd.DataFrame({'A': [np.nan, 'A1', 'A2', 'A3']},index=[1,2,3,4])
list(left['A'])


# In[207]:


#sort
#b[u'投信買賣超'].sort_values(ascending=False)
b

