import requests
from bs4 import BeautifulSoup
from django.utils.text import slugify
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView

from posts.models import Source, Post


class ScrapePostsView(GenericAPIView):
    new_posts_count = 0
    queryset = Source.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        for news_source in queryset:
            content = self.get_content(
                news_source.news_url,
                news_source.html_tag,
                news_source.html_tag_classes
            )
            self.parse(news_source, content)

    def get_content(self, web_page, tag, tag_class):
        web_page = requests.get(web_page)
        soup = BeautifulSoup(web_page.text, 'lxml')
        source = soup.find_all(tag, class_=tag_class)

        return source

    def parse(self, source: Source, news_source: list):
        for post in news_source:
            post_title = post.text
            post_image = post.find('img')
            post_image_src = '' if post_image is None else post_image.get(
                'src')
            post_link = post.a['href']
            if "https" not in post_link:
                post_link = source.domain + post_link

            post_exist = (
                Post.objects
                .filter(title=post_title, news_source=source)
                .first()
            )

            if not post_exist:
                Post.objects.create(
                    news_source=source,
                    title=post_title,
                    content=post_link,
                    image=post_image_src,
                    slug=slugify(post_title)
                )
                self.new_posts_count += 1

        return Response({
            "status": "success",
            "message": "New posts added successfully" if self.new_posts_count > 0 else "No posts found",
            "data": {
                "new_posts_count": self.new_posts_count
            }
        })
