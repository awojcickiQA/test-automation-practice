import pytest
from playwright.sync_api import APIRequestContext, expect

def test_get_all_posts(api_context: APIRequestContext):
    response = api_context.get("/posts")
    assert response.ok
    assert response.status == 200
    assert len(response.json()) == 100

def test_get_single_post(api_context: APIRequestContext):
    response = api_context.get("/posts/1")
    assert response.ok
    data = response.json()
    assert data["id"] == 1
    assert "title" in data
    assert "body" in data

def test_create_post(api_context: APIRequestContext):
    new_post = {
        "title": "foo",
        "body": "bar",
        "userId": 1
    }
    response = api_context.post("/posts", data=new_post)
    assert response.status == 201
    data = response.json()
    assert data["title"] == "foo"
    # JSONPlaceholder returns id 101 for new posts
    assert data["id"] == 101

def test_update_post(api_context: APIRequestContext):
    updated_post = {
        "id": 1,
        "title": "updated title",
        "body": "updated body",
        "userId": 1
    }
    response = api_context.put("/posts/1", data=updated_post)
    assert response.ok
    assert response.json()["title"] == "updated title"

def test_patch_post(api_context: APIRequestContext):
    response = api_context.patch("/posts/1", data={"title": "patched title"})
    assert response.ok
    assert response.json()["title"] == "patched title"

def test_delete_post(api_context: APIRequestContext):
    response = api_context.delete("/posts/1")
    assert response.status == 200 or response.status == 204
    # Note: JSONPlaceholder doesn't actually delete, it just simulates it

def test_get_post_comments(api_context: APIRequestContext):
    response = api_context.get("/posts/1/comments")
    assert response.ok
    assert len(response.json()) > 0

def test_filter_comments_by_post_id(api_context: APIRequestContext):
    response = api_context.get("/comments", params={"postId": 1})
    assert response.ok
    for comment in response.json():
        assert comment["postId"] == 1

def test_get_all_users(api_context: APIRequestContext):
    response = api_context.get("/users")
    assert response.ok
    assert len(response.json()) == 10

def test_get_all_albums(api_context: APIRequestContext):
    response = api_context.get("/albums")
    assert response.ok
    assert len(response.json()) == 100

def test_get_all_photos(api_context: APIRequestContext):
    response = api_context.get("/photos")
    assert response.ok
    assert len(response.json()) == 5000

def test_get_all_todos(api_context: APIRequestContext):
    response = api_context.get("/todos")
    assert response.ok
    assert len(response.json()) == 200
