from pathlib import Path
import datetime
import pytz
import feedparser


def update_footer():
    timestamp = datetime.datetime.now(
        pytz.timezone("Asia/Tehran")).strftime("%c")
    footer = Path('./FOOTER.md').read_text()
    return footer


def header():
    header = Path('./HEADER.md').read_text()
    return header


def update_readme_Pari_posts(Pari_post_path, readme_base, join_on):
    d = feedparser.parse(Pari_post_path)
    posts = []
    for item in d.entries:
        if item.get('tags'):
            posts.append(
                f'''- [{item['title']}]({item['link']})''')

    posts.append(
        '''<br><br>- *محتوا‌های مفید دیگر در [Parikhalegi.ir](https://parikhaleghi.ir)*''')
    posts_joined = '\n'.join(posts)
    return readme_base[:readme_base.find(rss_title_blog)] + f"{join_on}\n{posts_joined}"


def get_post_from_cpp_reference(Pari_cpp_post, readme_base, join_on):
    d = feedparser.parse(Pari_cpp_post)
    posts = []
    for item in d.entries:
        if item.get('title'):
            if f'''<a href="{item['link']}">{item['title']}</a>''' in posts:
                continue
            else:
                posts.append(
                    f'''<a href="{item['link']}">{item['title']}</a>''')

    posts.append(
        '''<br><p><i>More Contributing in <a href="https://en.cppreference.com/mwiki/index.php?limit=50&tagfilter=&title=Special%3AContributions&contribs=user&target=Parisakhaleghi&namespace=&year=&month=-1">cppreference</a></i></p>''')
    print(posts)
    posts_joined = '\n'.join(posts)
    return readme_base[:readme_base.find(rss_title_cppRef)] + f"{join_on}\n{posts_joined}"

with open("./README.md", "w") as f:
    pass

rss_title_blog = "### آخرین پست های وبلاگ"
rss_title_cppRef = "<h3>CppReference</h3><br>"
readme = Path('./README.md').read_text()
updated_readme_blog = update_readme_Pari_posts(
    "https://parikhaleghi.ir/feed/", readme, rss_title_blog)
add_cpp_reference = get_post_from_cpp_reference(
    "https://en.cppreference.com/mwiki/api.php?action=feedcontributions&user=Parisakhaleghi&feedformat=rss", readme, rss_title_cppRef)

with open('./README.md', "w+") as f:
    f.write(header() + updated_readme_blog + "<br><br>"
            + '''<div align="left">''' + add_cpp_reference + '''</div>''' + update_footer())


'''<a href="https://github.com/parikhaleghi/parikhaleghi/actions">
<img src="https://github.com/parikhaleghi/parikhaleghi/workflows/Build%20README/badge.svg" align="right" alt="Build README"></a> 
<a href="https://parikhaleghi.ir/2022/07/07/ci-cd/">How this works</a>'''
