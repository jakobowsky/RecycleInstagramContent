import json
import requests
from bs4 import BeautifulSoup


def profile_page_recent_posts(json_data_from_profile):
    results = []
    metrics = \
        json_data_from_profile['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media'][
            "edges"]
    for node in metrics:
        node = node.get('node')
        if node and isinstance(node, dict):
            try:
                if node['__typename'] == 'GraphImage':
                    post = {}
                    post['photo_url'] = node['display_url']
                    post['text'] = node['edge_media_to_caption']['edges'][0]['node']['text'].replace('\n', ' ')
                    results.append(post)
            except:
                pass
    return results


def get_instagram_posts_from_profile(username):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.11 (KHTML, like Gecko) '
                      'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }

    try:
        link = f"https://www.instagram.com/{username}/"
        response = requests.get(
            link,
            timeout=4,
            headers=headers,
        ).text
        json_data = extract_json_data(response)
    except Exception as e:
        raise e

    recent_posts = profile_page_recent_posts(json_data)
    return recent_posts


def extract_json_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find('body')
    script_tag = body.find('script')
    raw_string = script_tag.contents[0].strip().replace(
        'window._sharedData =', '').replace(';', '')

    return json.loads(raw_string)


def put_filter_on_photo(img_url):
    print(img_url)


def main():
    instagram_data = get_instagram_posts_from_profile('jakobowsky')
    for ig_post in instagram_data:
        put_filter_on_photo(ig_post['photo_url'])


if __name__ == '__main__':
    main()
