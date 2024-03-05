import logging
import re

import requests
from bs4 import BeautifulSoup

from apps.posts.models import Post, Source
from utils.get_images import get_post_images

logger = logging.getLogger(__name__)


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
    headers = get_headers()

    try:
        response = session.get(post.link_to_news, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        news_source = post.news_source

        post_content = soup.find_all(
            news_source.body_tag,
            class_=news_source.body_tag_class
        )

        if not post_content:
            post.delete()
            return False

        # Get images
        web_images = soup.find_all(
            news_source.image_tag,
            class_=news_source.image_tag_class
        )

        images_dict = {
            f"image_{index + 1}": image.img.get('src')
            for index, image in enumerate(web_images)
        }

        # Fetch additional images if less than 3
        if len(images_dict) < 3:
            sourced_images = get_post_images(post.title)
            images_dict.update(sourced_images)

        # Choose post body extraction method based on news source:
        # For some, only the first paragraph is relevant to the title,
        # while for others, all paragraphs are relevant.
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

    except requests.RequestException as e:
        logging.exception(e)
        return False


def get_post_list(sources: list[Source]) -> list:
    all_posts = []

    for source in sources:
        with requests.Session() as session:
            try:
                page_response = session.get(
                    source.news_page,
                    headers=get_headers()
                )
                soup = BeautifulSoup(page_response.text, 'lxml')
                posts = _create_post(source, soup)
                all_posts.extend(posts)
            except requests.ConnectTimeout as e:
                logger.exception(f"{source} is down again, sigh.")

    return all_posts


def _create_post(source: Source, soup: BeautifulSoup) -> None:
    """
    Creates a new post object based on the provided source and post data.
    """
    posts = []
    links = soup.find_all(source.link_tag, class_=source.link_tag_class)

    for link in links:
        title_element = link.find(source.title_tag)
        post_title = title_element.text.strip()
        post_link = link.get('href') or title_element.get('href', '')

        if not post_link.startswith("https"):
            post_link = source.domain + post_link

        existing_post = Post.objects.filter(
            link_to_news=post_link, news_source=source).first()

        if not existing_post:
            new_post = Post.objects.create(
                news_source=source,
                title=clean_text(post_title),
                body="...",
                link_to_news=post_link,
            )
            posts.append(new_post)

    return posts
