class ResponseTool:
    @classmethod
    def response2never_cache(cls, response):
        """
        Add headers to both force latest IE rendering engine or Chrome Frame,
        and also to cache the rendered page for 10 minutes.

        reference: https://stackoverflow.com/a/34067710/1902064
        reference: https://stackoverflow.com/a/46714639/1902064
        """
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

        return response
