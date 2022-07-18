from pathlib import Path
import datetime
import pytz
import feedparser


def update_footer():
    timestamp = datetime.datetime.now(
        pytz.timezone("Asia/Tehran")).strftime("%c")
    footer = Path('./FOOTER.md').read_text()
    return footer.format(timestamp=timestamp)


def header():
    header = Path('./HEADER.md').read_text()
    return header


def update_readme_Pari_posts(Pari_post_path, readme_base, join_on):
    d = feedparser.parse(Pari_post_path)
    posts = []
    for item in d.entries:
        if item.get('tags'):
            posts.append(
                f'''| [{item['title']}]({item['link']}) |''')

    posts.append(
        '''More Content in [Parikhalegi.ir](https://parikhaleghi.ir)''')
    posts_joined = '\n'.join(posts)
    return readme_base[:readme_base.find(rss_title_blog)] + f"{join_on}\n{posts_joined}"


def get_post_from_cpp_reference(Pari_cpp_post, readme_base, join_on):
    d = feedparser.parse(Pari_cpp_post)
    posts = []
    for item in d.entries:
        if item.get('title'):
            if f'''| [{item['title']}]({item['link']}) |''' in posts:
                continue
            else:
                posts.append(
                    f'''| [{item['title']}]({item['link']}) |''')

    posts.append(
        '''More Contributing in [cppreference](https://en.cppreference.com/mwiki/index.php?limit=50&tagfilter=&title=Special%3AContributions&contribs=user&target=Parisakhaleghi&namespace=&year=&month=-1)''')
    print(posts)
    posts_joined = '\n'.join(posts)
    return readme_base[:readme_base.find(rss_title_cppRef)] + f"{join_on}\n{posts_joined}"


with open("./README.md", 'w') as file:
    pass

rss_title_blog = "| آخرین پست های وبلاگ |"
rss_title_cppRef = "| CppReference |"
readme = Path('./README.md').read_text()
updated_readme_blog = update_readme_Pari_posts(
    "https://parikhaleghi.ir/feed/", readme, rss_title_blog)
add_cpp_reference = get_post_from_cpp_reference(
    "https://en.cppreference.com/mwiki/api.php?action=feedcontributions&user=Parisakhaleghi&feedformat=rss", readme, rss_title_cppRef)
with open('./README.md', "w+") as f:
    f.write(header()+ add_cpp_reference + '''<br> <br>\n'''
            +updated_readme_blog +update_footer())


'''<a href="https://github.com/simonw/simonw/actions">
<img src="https://github.com/simonw/simonw/workflows/Build%20README/badge.svg" align="right" alt="Build README"></a> 
<a href="https://simonwillison.net/2020/Jul/10/self-updating-profile-readme/">How this works</a>'''
