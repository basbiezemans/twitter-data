from TwitterAPI import TwitterPager

def filter_items(items):
    """ Filters a list of dictionaries by keys
    """
    keys = ['created_at', 'id', 'text']
    result = []
    for item in items:
        result.append({
            key: item.get(key) for key in keys
        })
    return result

def collect_tweets(twitter, queue):
    """ Collects a number of tweets and stores them in a text file
    """
    geocode, count, file_path = queue.get()
    iterator = TwitterPager(twitter, 'search/tweets', {'geocode': geocode}).get_iterator()
    k = 0
    with open(file_path, 'w', encoding='utf-8') as f:
        while k < count:
            k += 1
            item = next(iterator, {'message': 'sentinel'})
            if 'text' in item:
                # Remove extra whitespace and newlines
                line = ' '.join(item.get('text').split())
                print(line, file=f)
            elif 'message' in item:
                break
