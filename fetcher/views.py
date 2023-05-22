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

        def get_content(web_page, tag, tag_class):
            nonlocal new_posts_count

            web_page = requests.get(web_page)
            soup = BeautifulSoup(web_page.text, 'lxml')
            source = soup.find_all(tag, class_=tag_class)

            def parse(news_source):
                nonlocal new_posts_count

                for post in news_source:
                    post_title = post.text
                    post_link = post.a['href']

                    try:
                        Post.objects.get(title=post_title, news_source=news_source)
                    except Post.DoesNotExist:
                        Post.objects.create(
                            news_source=news_source,
                            title=post_title,
                            content=post_link,
                            slug=slugify(post_title)
                        )
                        new_posts_count += 1  # Increment the count of new posts

            parse(source)

        # Perform scraping
        for source in news_sources:
            get_content(source.news_url, source.html_tag, source.html_tag_classes)

        return Response({'new_posts_count': new_posts_count})
