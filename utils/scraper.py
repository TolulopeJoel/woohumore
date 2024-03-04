import contextlib
import re

import requests
from bs4 import BeautifulSoup

from apps.posts.models import Post, Source
from utils.get_images import get_post_images


def get_headers() -> dict:
    """
    Returns headers for making HTTP requests.
    """
    return {
        "User-Agent": "User-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }


def clean_text(text: str) -> str:
    """
    Cleans the given text by removing unwanted sentences,
    characters and symbols, and extra whitespaces.
    """
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'[^\x00-\x7F“”‘’"]+', ' ', text)
    text = re.sub(r'[\x80-\xFF]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r"(Published|Last updated) .* GMT ", '', text)
    text = re.sub(r"From .* inbox\.", '', text)
    text = re.sub(r"For more .* newsletter\.", '', text)
    text = re.sub(r"Topics: [^\n]+", '', text)

    return text


def get_post_detail(post: Post) -> bool:
    """
    Retrieves the body and images of a post from the
    specified web page, and updates the post object.
    """
    session = requests.Session()
    page_response = session.get(post.link_to_news, headers=get_headers())
    soup = BeautifulSoup(page_response.text, 'lxml')
    news_source = post.news_source

    # get post body and delete posts with no content
    post_content = soup.find_all(
        news_source.body_tag,
        class_=news_source.body_tag_class
    )
    if not post_content:
        post.delete()
        return False

    web_images = soup.find_all(
        news_source.image_tag,
        class_=news_source.image_tag_class
    )
    # if post images is less than 3,
    # fetch new images from external source.
    images_dict = {
        f"image_{index + 1}": image.img.get('src')
        for index, image in enumerate(web_images)
    }
    if len(images_dict) < 3:
        sourced_images = get_post_images(post.title)
        images_dict.update(sourced_images)

    # For some posts only the first paragraph relates to the title.
    # For others, all paragraphs relates to the title.
    # So, based on the news source, decide wether to get the
    # first paragraph or all paragraphs as the post body.
    for bunch_of_paragraphs in post_content:
        if news_source.find_all:
            all_paragraphs = bunch_of_paragraphs.find_all('p')
            all_paragraphs = [p.text for p in all_paragraphs]
            post_body = " ".join(all_paragraphs)
        else:
            first_paragraph = bunch_of_paragraphs.find('p')
            post_body = first_paragraph.text

    post.body = clean_text(post_body)
    post.images = images_dict
    post.has_body = True
    post.save()
    return True


def get_post_list(sources: list[Source]) -> None:
    for source in sources:
        session = requests.Session()
        page_response = session.get(
            source.news_page, headers=get_headers()
        )
        # silence error when connection times out
        with contextlib.suppress(requests.exceptions.ConnectTimeout):
            soup = BeautifulSoup(page_response.text, 'lxml')
            _create_post(source, soup)


def _create_post(source: Source, soup: BeautifulSoup) -> None:
    """
    Creates a new post object based on the provided source and post data.
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
                title=clean_text(post_title),
                body="None",
                link_to_news=post_link,
            )
            new_post.save()
