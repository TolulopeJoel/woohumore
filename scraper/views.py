import requests
from bs4 import BeautifulSoup
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from posts.models import Post, Source
from posts.views import SourceViewset


class ScrapePostListView(GenericAPIView):
    new_posts_count = 0
    queryset = SourceViewset.get_queryset(SourceViewset)

    def get(self, request, *args, **kwargs):
        """
        Retrieves news posts from the specified sources,
        creates post objects, and returns a response with the count of new posts.
        """
        queryset = self.get_queryset()

        for source in queryset:
            headers = {
                "User-Agent": "User-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            }
            session = requests.Session()
            page_response = session.get(source.news_page, headers=headers)
            soup = BeautifulSoup(page_response.text, 'lxml')
            self.create_post(source, soup)

        response_data = {
            "status": "success",
            "message": "New posts added successfully" if self.new_posts_count > 0 else "No news posts found",
            "data": {
                "new_posts_count": self.new_posts_count
            }
        }

        return Response(response_data)

    def create_post(self, source: Source, soup):
        """
        Creates a new post object based on the provided source and post data.

        Args:
            source (Source): The source of the post.
            post (BeautifulSoup): The BeautifulSoup element representing the post.

        Returns:
            None

        """
        links = soup.find_all(source.link_tag, class_=source.link_tag_class)

        for link in links:
            title = link.find(source.title_tag) if link else None
            post_title = title.text.strip()

            if (post_link := link.get('href')) is None:
                post_link = title.get('href')

            if not post_link.startswith("https"):
                post_link = source.domain + post_link

            post_exist = Post.objects.filter(
                link_to_news=post_link, news_source=source).first()

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
        headers = {
            "User-Agent": "User-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }
        session = requests.Session()
        page_response = session.get(post.link_to_news, headers=headers)
        soup = BeautifulSoup(page_response.text, 'lxml')

        source = post.news_source
        images = soup.find_all(
            source.image_tag, class_=source.image_tag_class
        )
        _images = {
            f"image_{index + 1}": image.img.get('src')
            for index, image in enumerate(images)
        }
        body = soup.find_all(source.body_tag, class_=source.body_tag_class)
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
