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
                f'''- <a href="{item['link']}">{item['title']}</a><br><br>''')

    posts.append(
        '''مطالب بیشتر در <a href="https://parikhaleghi.ir">Parikhalegi.ir</a>''')
    posts_joined = '\n'.join(posts)
    return readme_base[:readme_base.find(rss_title_blog)] + f"{join_on}\n{posts_joined}"


def get_post_from_cpp_reference(Pari_cpp_post, readme_base, join_on):
    d = feedparser.parse(Pari_cpp_post)
    posts = []
    for item in d.entries:
        if item.get('title'):
            if f'''- <a href="{item['link']}">{item['title']}</a><br><br>''' in posts:
                continue
            else:
                posts.append(
                    f'''- <a href="{item['link']}">{item['title']}</a><br><br>''')

    posts.append(
        '''مطالب بیشتر در <a href="https://en.cppreference.com/mwiki/index.php?limit=50&tagfilter=&title=Special%3AContributions&contribs=user&target=Parisakhaleghi&namespace=&year=&month=-1">cppreference</a>''')
    print(posts)
    posts_joined = '\n'.join(posts)
    return readme_base[:readme_base.find(rss_title_cppRef)] + f"{join_on}\n{posts_joined}"


with open("./README.md", 'w') as file:
    pass

header_readme = '''<h1><a href="parikhalegi.ir">Parikhalegi</a> & <a href="https://en.cppreference.com/w/">cppreference</a>'''
rss_title_blog = "<h4>آخرین پست های وبلاگ</h4>"
rss_title_cppRef = "<h4>CppReference</h4>"
readme = Path('./README.md').read_text()
updated_readme_blog = update_readme_Pari_posts(
    "https://parikhaleghi.ir/feed/", readme, rss_title_blog)
add_cpp_reference = get_post_from_cpp_reference(
    "https://en.cppreference.com/mwiki/api.php?action=feedcontributions&user=Parisakhaleghi&feedformat=rss", readme, rss_title_cppRef)
with open('./README.md', "w+") as f:
    f.write('''<div align="center"><table><tr><td align="left" valign="top" width="33%">'''+add_cpp_reference + '''</td><br> <br>\n''' +
            '''<td align="right" valign="top" width="33%">'''+updated_readme_blog + '''</td></tr></table></div>''' + update_footer())
