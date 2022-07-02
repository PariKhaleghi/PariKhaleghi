from pathlib import Path
import datetime
import pytz
import feedparser


def update_footer():
    timestamp = datetime.datetime.now(
        pytz.timezone("Asia/Tehran")).strftime("%c")
    footer = Path('./FOOTER.md').read_text()
    return footer.format(timestamp=timestamp)


def update_readme_medium_posts(Pari_post_path, readme_base, join_on):
    d = feedparser.parse(Pari_post_path)
    posts = []
    for item in d.entries:
        if item.get('tags'):
            posts.append(f"- [{item['title']}]({item['link']})")
    posts_joined = '\n'.join(posts)
    return readme_base[:readme_base.find(rss_title)] + f"{join_on}\n{posts_joined}"


rss_title = "### آخرین پست های پریسا در [parikhaleghi.ir](https://parikhaleghi.ir)"
readme = Path('./README.md').read_text()
updated_readme = update_readme_medium_posts(
    "https://parikhaleghi.ir/feed/", readme, rss_title)
with open('./README.md', "w+") as f:
    f.write(updated_readme + update_footer())
