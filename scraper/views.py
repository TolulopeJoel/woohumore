import requests
from bs4 import BeautifulSoup
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from posts.models import Post, Source


class ScrapePostListView(GenericAPIView):
    new_posts_count = 0
    queryset = Source.objects.filter(active=True)

    def get(self, request, *args, **kwargs):
        """
        Retrieves news posts from the specified sources,
        creates post objects, and returns a response with the count of new posts.
        """
        queryset = self.get_queryset()

        for source in queryset:
            news_posts = self.get_posts(
                source.news_page,
                source.html_tag,
                source.html_tag_classes
            )

            for post in news_posts:
                self.create_post(source, post)

        response_data = {
            "status": "success",
            "message": "New posts added successfully" if self.new_posts_count > 0 else "No news posts found",
            "data": {
                "new_posts_count": self.new_posts_count
            }
        }

        return Response(response_data)

    def get_posts(self, web_page, tag, tag_class):
        """
        Retrieves posts from a web page based on the specified tag and class.

        Args:
            web_page (str): The URL of the web page to scrape.
            tag (str): The HTML tag of the elements to search for.
            tag_class (str): The class attribute of the elements to search for.

        Returns:
            list: A list of BeautifulSoup elements representing the posts found on the web page.

        """
        web_page_response = requests.get(web_page)
        soup = BeautifulSoup(web_page_response.text, 'lxml')
        return soup.find_all(tag, class_=tag_class)

    def create_post(self, source, post):
        """
        Creates a new post object based on the provided source and post data.

        Args:
            source (Source): The source of the post.
            post (BeautifulSoup): The BeautifulSoup element representing the post.

        Returns:
            None

        """
        post_title = post.text
        post_link = post.a['href']

        if not post_link.startswith("https"):
            post_link = source.domain + post_link

        post_exist = Post.objects.filter(
            title=post_title, news_source=source).first()

        if not post_exist:
            new_post = Post(
                news_source=source,
                title=post_title,
                body="None",
                link_to_news=post_link,
            )
            new_post.save()

            self.new_posts_count += 1
