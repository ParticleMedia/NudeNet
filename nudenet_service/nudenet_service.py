import aiohttp.web
from simple_celery.service_util.network_util import get_ip
from nudenet import NudeClassifier
from simple_celery.utils.download_util import download


class NudenetService:

    def __init__(self):
        self.classifier = NudeClassifier()

    async def post(self, req: aiohttp.web.Request):
        request = await req.json()
        image_path = request.pop('image_path', None)
        if image_path is None:
            reply = {}
        else:
            reply = self.classify(image_path)
        return aiohttp.web.json_response(reply)

    def classify(self, image_path):
        if image_path.startswith("http"):
            image_bytes = download(image_path)
            if image_bytes is None:
                return {}
            result = self.classifier.classify(image_bytes)
            result = result.get(0)
        else:
            result = self.classifier.classify(image_path)
            result = result.get(image_path)
        if result is None:
            return {}
        result_1 = {}
        for k, v in result.items():
            try:
                result_1.update({k: float(v)})
            except:
                pass
        return result_1

    @staticmethod
    def set_http_service(port):
        host = get_ip()
        service = NudenetService()
        app = aiohttp.web.Application()
        app.add_routes([aiohttp.web.post('/', service.post)])
        aiohttp.web.run_app(app, port=port, host=host)


if __name__ == "__main__":
    NudenetService.set_http_service(port=4500)
