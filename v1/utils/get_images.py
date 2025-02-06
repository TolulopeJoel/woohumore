from services.freepik import FreePikService
from services.shutterstock import ShutterStockService


def get_post_images(search_text):
    # use service based on image service priority
    shutterstock = ShutterStockService()
    images = shutterstock.get_images(search_text)
 
    if len(images) < 3:
        freepik = FreePikService()
        freepik_images = freepik.get_images(search_text)
        if freepik_images:
            images.update(freepik_images)

    return images
