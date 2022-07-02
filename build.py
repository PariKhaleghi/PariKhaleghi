from pathlib import Path
import datetime
import pytz

import feedparser


def update_footer():
    timestamp = datetime.datetime.now(
        pytz.timezone("Europe/Madrid")).strftime("%c")
    footer = Path('./FOOTER.md').read_text()
    return footer.format(timestamp=timestamp)


def update_readme_medium_posts(Pari_post_path, readme_base, join_on):
    d = feedparser.parse(Pari_post_path)
    posts = []
    for item in d.entries:
        posts.append("""<td valign="top" width="33%">""")
        if item.get('tags'):
            posts.append(f"- [{item['title']}]({item['link']})")
        posts.append("""<td/>""")
    posts_joined = '\n'.join(posts)
    return readme_base[:readme_base.find(rss_title)] + f"{join_on}\n{posts_joined}"


rss_title = "### آخرین پست های من در "
readme = Path('./README.md').read_text()
updated_readme = update_readme_medium_posts(
    "https://medium.com/feed/@dylanroy", readme, rss_title)
with open('./README.md', "w+") as f:
    f.write(updated_readme + update_footer())
