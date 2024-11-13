import json

POSTS_FILE = './app/posts/posts.json'

def load_posts() -> list[dict]:    
    with open(POSTS_FILE, 'r') as f:
        try:
            posts = json.load(f)
            print("Loaded posts:", posts) 
            return posts
        except json.decoder.JSONDecodeError:
            print("Error: The JSON file is malformed.")
            return []

def save_post(post: dict):
    posts = load_posts()
    posts.append(post)
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f, indent=4)


def get_post(id: int):
    all_posts = load_posts()
    post = next((post for post in all_posts if post["id"] == id), None)
    return post