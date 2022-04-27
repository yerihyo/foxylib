class GoogleTool:
    @classmethod
    def profile_image_url2norm(cls, image_url: str) -> str:
        if not image_url:
            return image_url

        index = image_url.rfind('=')
        if index < 0:
            return image_url

        return image_url[:index]
