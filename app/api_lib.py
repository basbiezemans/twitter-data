
# Filter a Twitter response dictionary by keys
def filter_response(r):
    keys = ['created_at', 'id', 'text']
    tweets = []
    for item in r:
        tweets.append({
            key: item.get(key) for key in keys
        })
    return tweets