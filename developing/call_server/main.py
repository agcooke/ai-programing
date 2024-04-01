import requests


def get_server_hello_world():
    url = "http://server:8080"  # The URL of your server
    response = requests.get(url)

    if response.status_code == 200:
        print("Successfully connected to the server. Here's the response:")
        print(response.text)
    elif response.status_code == 404:
        print("Error: Resource not found on the server.")
    else:
        print(f"Error: Received status code {response.status_code} from the server.")


if __name__ == "__main__":
    get_server_hello_world()
