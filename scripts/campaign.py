import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('data/clean_data.csv')
def site_scores(campaignid:str):
    campaign = df.loc[df['CampaignId']== campaignid]
    campaign.drop(['CampaignId'],axis = 1, inplace = True)
    site = campaign.groupby('Site').agg({'AdGroupId':'mean','AudienceID':'mean','AdFormat':'mean','FoldPosition':'mean', 'Region':'mean',
    'City':'mean', 'DeviceType':'mean', 'OSFamily':'mean', 'OS':'mean','Browser':'mean',
    'DeviceMake':'mean', 'AdvertiserCurrency':'mean', 'click':'mean', 'engagement':'mean',
    'video-end':'mean', 'video-start':'mean', 'engagement_rate':'mean', 'hour':'mean'}).reset_index()
    #site.drop('Site',axis = 1, inplace = True)
    site.loc[site['engagement'] < 0.5, 'engagement'] = 0
    site.loc[site['engagement'] >= 0.5, 'engagement'] = 1
    X = site.drop(['engagement','Site'], axis = 1)
    y = site['engagement']
    model = LogisticRegression(max_iter=1000)
    model.fit(X,y)
    scores = model.predict_proba(X)[:,1]*100

    sites =pd.DataFrame(site.Site)
    score = pd.DataFrame(scores)
    data = pd.concat([sites,score],axis = 1)
    data.columns = ['Site','Score']
    data.Score = data.Score.round(2)
    data.sort_values(by = 'Score', ascending = False, inplace = True)
    data.reset_index(drop = True,inplace = True)
    
    return data
