import requests

url = "https://getpantry.cloud/apiv1/pantry/c96b7120-d350-4ac1-af69-1bee5f3554d3/basket/CrosshellVerifierNameList"
headers = {"Content-Type": "application/json"}
data = {"gAAAAABj6DuEB1yozWQCDWzl_ckPU5UZxPS3XKHmjgRvXhDaZ7pbLjD60b-z-BojORQX-aWek5mnEeNUTG6Hn8PzsUB_70eXTg==": "gAAAAABj6DuErTtjiDDtV1EYF-XuzwGZ49rjsuW0iiaB3nzHQ7jAOQbkm7PYwboLcQzcEkUtMghXGGJeJBkCkM9cq0U7GSUV0vAwWa719HN4E55aPvXekno="}
print(type(data))
response = requests.put(url, headers=headers, json=data)
print(response.content)