from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import requests

# gunicorn
app = Flask(__name__)
CORS(app, resources=r'/*')
app.config.from_pyfile("settings.py")


@app.route('/page/metrics', methods=['GET', "POST"])
def page_metrics():
    object_id = ""
    url = f'https://graph.facebook.com/v17.0/{object_id}/insights'
    result = {}

    if app.config['DEBUG']:
        result = {'impressions': 13323, 'engaged_accounts': 11234, 'profile_views': 23123}
    else:
        access_token = app.config['DEBUG']
        param = {'access_token': access_token,
                 'metric': "page_impressions*,page_engaged_users,page_views_by_profile_tab_total"}

        res = requests.get(url, param).json()
        impressions = -1
        engaged_accounts = -1
        profile_views = -1

        for metric in res['data']:
            if "page_impressions*" in metric:
                impressions = metric['page_impressions*']
            if "page_engaged_users" in metric:
                engaged_accounts = metric['page_engaged_users']
            if "page_views_by_profile_tab_total" in metric:
                profile_views = metric['page_views_by_profile_tab_total']

        result = {'impressions': impressions, 'engaged_accounts': engaged_accounts,
                  'profile_views': profile_views}
    response = make_response(jsonify(result))
    return response


@app.route('/post/metrics', methods=['GET', "POST"])
def post_metrics():
    object_id = ""
    url = f'https://graph.facebook.com/v17.0/{object_id}/insights'
    result = {}

    if app.config['DEBUG']:
        result = {'comments': 3323, 'likes': 1234, 'shares': 2123,
                  'replies': 3323, 'post_impressions': 1234, 'post_reach': 2123,
                  'post_clicks': 3323, 'post_engagements': 1234
                  }
    else:
        access_token = app.config['DEBUG']
        param = {'access_token': access_token,
                 'metric': "comment,like,link,rsvp,page_posts_impressions*,page_posts_impressions_unique,post_clicks*,post_engaged_users"}

        res = requests.get(url, param).json()

        comments = -1
        likes = -1
        shares = -1
        replies = -1
        post_impressions = -1
        post_reach = -1
        post_clicks = -1
        post_engagements = -1

        for metric in res['data']:
            if "comment" in metric:
                comments = metric['comment']
            if "like" in metric:
                likes = metric['like']
            if "link" in metric:
                shares = metric['link']
            if "rsvp" in metric:
                replies = metric['rsvp']
            if "page_impressions" in metric:
                post_impressions = metric['page_posts_impressions*']
            if "page_posts_impressions_unique" in metric:
                post_reach = metric['page_posts_impressions_unique']
            if "post_clicks*" in metric:
                post_clicks = metric['post_clicks*']
            if "post_engaged_users" in metric:
                post_engagements = metric['post_engaged_users']

        result = {'comments': comments, 'likes': likes, 'shares': shares,
                  'replies ': replies, 'post_impressions': post_impressions, 'post_reach': post_reach,
                  'post_clicks': post_clicks,
                  'post_engagements': post_engagements}
    response = make_response(jsonify(result))
    return response


@app.route('/video/metrics', methods=['GET', "POST"])
def video_metrics():
    AD_ACCOUNT_ID = ""
    url = f'https://graph.facebook.com/v17.0/act_{AD_ACCOUNT_ID}/ad_studies'
    result = {}

    if app.config['DEBUG']:
        result = {'video_views': 3323, 'average_watch_time': 1234, 'video_shares': 2123,
                  'comments': 3323}
    else:
        access_token = app.config['DEBUG']
        param = {'date_preset': 'last_30_days', 'access_token': access_token,
                 'fields': "actions, video_avg_pct_watched_actions, video_complete_watched_actions"}
        res = requests.get(url, param).json()
        video_views = -1
        average_watch_time = -1
        video_shares = -1
        comments = -1
        for action in res['data'][0]['actions']:
            if action['action_type'] == 'video_view' and action['action_video_type'] == 'total':
                video_views = action['value']
        for action in res['data'][0]['video_avg_pct_watched_actions']:
            if action['action_type'] == 'video_view' and action['action_video_type'] == 'total':
                average_watch_time = action['value']

        result = {'video_views': video_views, 'average_watch_time': average_watch_time, 'video_shares': video_shares,
                  'comments ': comments}

    response = make_response(jsonify(result))
    return response


@app.route('/ad/metrics', methods=['GET', "POST"])
def ad_metrics():
    AD_SET_ID = ""
    url = f'https://graph.facebook.com/v17.0/{AD_SET_ID}/ad_studies'
    result = {}

    if app.config['DEBUG']:
        result = {'ad_impressions': 1323, 'ad_clicks': 1234, 'ad_conversions': 213,
                  'ad_spend': 13323}
    else:
        access_token = app.config['DEBUG']
        param = {'access_token': access_token,
                 'fields': "impresssions, clicks, conversions,spend"}

        res = requests.get(url, param).json()
        ad_impressions = -1
        ad_clicks = -1
        ad_conversions = -1
        ad_spend = -1

        for metric in res['data']:
            if "impressions" in metric:
                ad_impressions = metric['impressions']
            if "impressions" in metric:
                ad_clicks = metric['clicks']
            if "conversions" in metric:
                ad_conversions = metric['conversions']
            if "spend" in metric:
                ad_spend = metric['spend']

        result = {'ad_impressions': ad_impressions, 'ad_clicks': ad_clicks, 'ad_conversions': ad_conversions,
                  'ad_spend ': ad_spend}
    response = make_response(jsonify(result))
    return response


if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0")
