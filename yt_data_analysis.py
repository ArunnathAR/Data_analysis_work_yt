#Youtube data analysis
#Open jupyter notebook

from googleapiclient.discovery import build
import pandas as p

Api_key_value='YYYYYYYYYYYYYYYYYYYYYYYY' # your youtube api data key
youtubechannel_id = ['UCq-Fj5jknLsUf-MWSy4_brA',]

#from youtube api data
#using the below code to use the api

api_service_name = "youtube"
api_version = "v3"

# Get credentials and create an API client

youtube = build(
    api_service_name, api_version, developerKey=Api_key_value)

#for channel videos to  dataframe

def channel_info(youtube,youtubechannel_id):
    
    new_data=[]
    
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=",".join(youtubechannel_id)
        
    )
    response = request.execute()

    for i in response['items']:
        d={'Youtubechannel_name':i['snippet']['title'],
          'subscribers_count':i['statistics']['subscriberCount'],
          'No_of_views':i['statistics']['viewCount'],
          'total_views':i['statistics']['videoCount'],
          'playlist_Id':i['contentDetails']['relatedPlaylists']['uploads']}
        
        new_data.append(d)
        
    return(p.DataFrame(new_data))

video_stats = channel_info(youtube,youtubechannel_id)
print(video_stats)

#for playlist items to dataframe


def video_id(youtube,playId):
    
    Avideo_id=[]
    

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playId,
        maxResults=50
        
    )
    responed=request.execute()
    
    for j in responed['items']:
        Avideo_id.append(j['contentDetails']['videoId'])
        
    nxt_page_token = responed.get('nextPageToken')
    
    while nxt_page_token is not None:
        request = youtube.playlistItems().list(
                    part="contentDetails",
                    playlistId=playId,
                    maxResults=50,
                    pageToken=nxt_page_token)
        
        responed=request.execute()
    
        for j in responed['items']:
            Avideo_id.append(j['contentDetails']['videoId'])
        
        nxt_page_token = responed.get('nextPageToken')
        
        
    return Avideo_id

playId="UUoOae5nYA7VqaXzerajD0lg"


vid_id = video_id(youtube,playId)

print(vid_id)

'''def comment_video(youtube,vid_id):
    
    a_comment=[]
    
    for vid_ids in vid_id:
        
        request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=vid_id)
        responed=request.execute()
        
        c_v=[comment['snippet']['topLevelComment']['snippet']['textOriginal'] for comment in responed]
        
        c_v_i={'video_id':vid_ids,'comments':c_v}
        
        a_comment.append(c_v_i)
        
    return p.DataFrame(a_comment)

c_df = comment_video(youtube,vid_id)
c_df
c_df['comments'][0] '''

    
def videodetails(youtube,video_ids):
    

    all_video_information=[]
    
    for i in range(0,len(video_ids),50):

        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=vid_id[i:i+50]
        )
        responed = request.execute()
    for video in responed['items']:
        stats= {'snippet':['channelTitle','title','description','tags','publishedAt'],
               'statistics':['viewCount','likeCount','favouriteCount','commentCount'],
               'contentDetails':['duration','defanition','caption']}
    
        video_information= {}
        video_information['video_id']=video['id']
    
        for k in stats.keys():
            for l in stats[k]:
                try:
                    video_information[l]=video[k][l]
                except:
                    video_information[k]=None
                
        all_video_information.append(video_information)
        
    return p.DataFrame(all_video_information)
vid_df = videodetails(youtube,vid_id)
print(vid_df)

#youtube channel data has printed

vid_df.isnull().any()
#null values

#data analytics 

n=['viewCount','likeCount','favouriteCount','commentCount']
vid_df[n]=vid_df[n].apply(p.to_numeric,errors='coerce',axis=1)

#date and time analytics 
from dateutil import parser
vid_df['publishedAt'] = vid_df['publishedAt'].apply(lambda y: parser.parse(y))
vid_df['publishDayName']=vid_df['publishedAt'].apply(lambda y:y.strftime("%A"))

#video running time analytics
import isodate
vid_df['durationSecs']=vid_df['duration'].apply(lambda y: isodate.parse_duration(y))
vid_df['durationSecs']=vid_df['durationSecs'].astype('timedelta64[s]')

print(vid_df[['durationSecs','duration']])

#data visualization
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
a=sns.barplot(x='title',y='viewCount',data=vid_df.sort_values('viewCount',ascending=False))
plot=a.set_xticklabels(a.get_xticklabels(),rotation=90)
a.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos:'{:,.0f}'.format(x/1000)+'K'))

#barplot

a=sns.barplot(x='title',y='viewCount',data=vid_df.sort_values('viewCount',ascending=true))
plot=a.set_xticklabels(a.get_xticklabels(),rotation=90)
a.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos:'{:,.0f}'.format(x/1000)+'K'))

#violinplot 

sns.violinplot(vid_df['channelTitle'],vid_df['viewCount'])

#scatterplotting
fig,a=plt.subplote(1,2)
sns.scatterplot(data=vid_df,x='commentCount',y='viewCount',a=a[0])
sns.scatterplot(data=vid_df,x='likeCount',y='viewCount',a=a[1])

#histplot
sns.hisplot(data=vid_df,x='durationSecs',bins=30)

#the aim is to increases the channel subscribers and viewers by comparing with other content creators
