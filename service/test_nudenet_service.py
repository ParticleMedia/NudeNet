import requests
from simple_celery.service_util.http_service_util import parse_http_result


def test_nudenet_service(image_path):
    response = requests.post("http://127.0.0.1:4500", json={'image_path': image_path})
    _, response = parse_http_result(response)
    print(response)


if __name__ == "__main__":
    test_nudenet_service('https://static.amazon.jobs/teams/479/images/Software_Development_1440.jpg?1590780674')
    test_nudenet_service('/Users/chengniu/Desktop/images/rga6845.jpeg')