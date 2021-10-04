from flask import Flask, make_response, request, jsonify
from flask_restplus import Api, Resource, fields
import pandas as pd
from sklearn.linear_model import LogisticRegression
import numpy as np
import sys

df = pd.read_csv('../data/clean_data.csv')
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
    model = LogisticRegression()
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
    
app = Flask(__name__)
api = Api(app = app,version = "1.0",title = "Top sites per campaign", 
description = "Displays the top sites per selected Campaign")

name_space = api.namespace('campaign', description='Campaign APIs')

model = api.model('Campaign params', {'campaign_id': fields.String(required = True,
description="Campaign_ID", help="Campaign cannot be blank")})

@app.route('/', methods = ['GET', 'POST'])

def home():
    output = None
    if request.method == 'POST':
        user_input = request.form.get('campaign')
        output = site_scores(user_input)
        output = output.apply(lambda x: x.to_json(), axis=1) 
    else:
        output = None
    return jsonify(output)
if __name__=='__main__':
    app.run(debug=True)