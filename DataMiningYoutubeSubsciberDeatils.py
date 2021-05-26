# while generating the clientSecretFile in oAuthConsent developer should be given access under testing,should be added there.
# Also we get the details of subscribers who set their subscriptions visibility to public.
def getSubscriberDetails(developerKey, channelId, clientSecretFile):
    import os
    import google.oauth2.credentials
    import google_auth_oauthlib.flow
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow

    youtube = build('youtube', 'v3', developerKey=developerKey)  # getting the subscriberCount from channelsAPI
    subcribersCount = youtube.channels().list(part='statistics', id=channelId).execute()['items'][0]['statistics'][
        'subscriberCount']  # UCnprfRlJB7WE6zAEaOAfVYA
    subcribersCount = (int(subcribersCount) // 10 + 1) * 10  # make it a multiple of ten

    SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'
    subscriber_list = []

    def get_authenticated_service():
        flow = InstalledAppFlow.from_client_secrets_file(clientSecretFile, SCOPES)
        credentials = flow.run_console()
        return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    # Remove keyword arguments that are not set
    def remove_empty_kwargs(**kwargs):
        good_kwargs = {}
        if kwargs is not None:
            for key, value in kwargs.items():
                if value:
                    good_kwargs[key] = value
        return good_kwargs

    def subscriptions_list_by_channel_id(client, **kwargs):
        kwargs = remove_empty_kwargs(**kwargs)
        response = client.subscriptions().list(**kwargs).execute()  # this gives the subscribersSnippet
        return response

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    client = get_authenticated_service()

    def tempList(response):  # gives a list of dictonaries which contains name and channelId of subscribers.
        _list = []
        for i in response['items']:
            subscriber_dict = {}
            subscriber_dict["Name"] = i['subscriberSnippet']['title']
            subscriber_dict['channelId'] = i['subscriberSnippet']['channelId']
            _list.append(subscriber_dict)
        return _list

    for i in range(subcribersCount):  # we iterate the subscribersSnippet and iterate based on subscriberCount
        if i == 0:
            response = subscriptions_list_by_channel_id(client, part='subscriberSnippet', mySubscribers=True,
                                                        maxResults=50)
            subscriber_list.extend(
                tempList(response))  # extending the list for adding the subsequent response.
            try:
                Token = response[
                    'nextPageToken']  # if nextpagetoken is available in the response ,will only be available when the subcribercount is more.
            except:
                break
        else:
            response = subscriptions_list_by_channel_id(client, part='subscriberSnippet', mySubscribers=True,
                                                        maxResults=10, pageToken=Token)
            subscriber_list.extend(tempList(
                response))  # getting the response if the nextpage token is available and if it's the last page we break.
            try:
                Token = response['nextPageToken']
            except:
                break

    return subscriber_list

print(getSubscriberDetails(developerKey='AIzaSyBpTWVW9z8nuPHvuVtxIyU6fOJqlSRVmiU',channelId='UCAmbsgvOnM6-9eU3GqI9mUQ',clientSecretFile="C:\\Users\\dell\\Downloads\\client_secret_936337865172-kk3hhfrak97bcpgqhs734o744r93o6sk.apps.googleusercontent.com.json"))
