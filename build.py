from pathlib import Path
import datetime
import pytz
import feedparser


def update_footer():
    timestamp = datetime.datetime.now(
        pytz.timezone("Asia/Tehran")).strftime("%c")
    footer = Path('./FOOTER.md').read_text()
    return footer.format(timestamp=timestamp)


def update_readme_Pari_posts(Pari_post_path, readme_base, join_on):
    d = feedparser.parse(Pari_post_path)
    posts = []
    for item in d.entries:
        if item.get('tags'):
            posts.append(
                f"- [{item['title']}]({item['link']}) - {item['updated']}")
    posts_joined = '\n'.join(posts)
    return readme_base[:readme_base.find(rss_title_blog)] + f"{join_on}\n{posts_joined}"


def get_post_from_cpp_reference(Pari_cpp_post, readme_base, join_on):
    d = feedparser.parse(Pari_cpp_post)
    posts = []
    for item in d.entries:
        if item.get('title'):
            posts.append(
                f"- [{item['title']}]({item['link']}) - {item['updated']}")

    for i in range(0, len(posts)):
        for j in range(i+1, len(posts)):
            if(j >= len(posts)):
                break
            if(posts[i] == posts[j]):
                objectt = str(posts[i])
                posts.remove(objectt)

    print(posts)
    posts_joined = '\n'.join(posts)
    return readme_base[:readme_base.find(rss_title_cppRef)] + f"{join_on}\n{posts_joined}"


rss_title_blog = "### آخرین پست های پریسا در [parikhaleghi.ir](https://parikhaleghi.ir)"
rss_title_cppRef = "### آخرین پست های پریسا در [cppreference.com ](https://cppreference.com)"
readme = Path('./README.md').read_text()
updated_readme_blog = update_readme_Pari_posts(
    "https://parikhaleghi.ir/feed/", readme, rss_title_blog)
add_cpp_reference = get_post_from_cpp_reference(
    "https://en.cppreference.com/mwiki/api.php?action=feedcontributions&user=Parisakhaleghi&feedformat=rss", readme, rss_title_cppRef)
with open('./README.md', "w+") as f:
    f.write(add_cpp_reference + "<br> <br>\n" +updated_readme_blog + update_footer())
