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


class ScrapePostDetailView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.filter(no_body=True)
        for post in queryset:
            self.get_body_n_image(post)

        return Response({
            "status": "success",
            "message": "Post content added successfully",
        })

    def get_body_n_image(self, post):
        """
        Retrieves the body and images of a post from the specified web page,
        updates the post object, and returns a boolean indicating success.

        Args:
            post (Post): The post object to update.

        Returns:
            bool: True if the body and images were successfully retrieved and updated,
                False otherwise.

        """

        web_page_response = requests.get(post.link_to_news)
        soup = BeautifulSoup(web_page_response.text, 'lxml')

        source = post.news_source
        images = soup.find_all(
            source.image_tag, class_=source.image_tag_classes
        )
        _images = {
            f"image_{index + 1}": image.img.get('src')
            for index, image in enumerate(images)
        }
        body = soup.find_all(source.body_tag, class_=source.body_tag_classes)
        if body == []:
            post.delete()
            return False

        for texts in body:
            paragraphs = texts.find_all('p')
            paragraphs = [p.text for p in paragraphs]
            _body = "\n\n".join(paragraphs)

        post.body = _body
        post.images = _images
        post.no_body = False
        post.save()
        return True
