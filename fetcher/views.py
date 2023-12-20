import requests
from bs4 import BeautifulSoup
from django.utils.text import slugify
from rest_framework.response import Response
from rest_framework.views import APIView

from news.models import NewsSource, Post


class ScrapeAndCountPostsView(APIView):
    def get(self, request, *args, **kwargs):
        news_sources = NewsSource.objects.all()
        new_posts_count = 0  # Initialize the count of new posts

        def get_content(instance, web_page, tag, tag_class):
            nonlocal new_posts_count

            web_page = requests.get(web_page)
            soup = BeautifulSoup(web_page.text, 'lxml')
            source = soup.find_all(tag, class_=tag_class)

            def parse(news_source):
                nonlocal new_posts_count

                for post in news_source:
                    post_title = post.text
                    post_image = post.find('img')
                    post_image_src = '' if post_image is None else post_image.get('src')
                    post_link = post.a['href']
                    if "https" not in post_link:
                        post_link = instance.site_domain + post_link

                    post_exist = (
                        Post.objects
                        .filter(title=post_title, news_source=instance)
                        .first()
                    )

                    if not post_exist:
                        Post.objects.create(
                            news_source=instance,
                            title=post_title,
                            content=post_link,
                            image=post_image_src,
                            slug=slugify(post_title)
                        )
                        new_posts_count += 1
            parse(source)

        for source in news_sources:
            get_content(
                source,
                source.news_url,
                source.html_tag,
                source.html_tag_classes
            )

        return Response({'new_posts_count': new_posts_count})
