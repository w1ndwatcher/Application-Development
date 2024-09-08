
# Flask Blogging App
A blogging app to create and manage posts.


## Run Locally

```bash
    pip install -r requirements.txt
```

Export Flask app 

```bash
    export FLASK_APP=main.py
    export FLASK_ENV=development

```

Run the Server
```bash
    flask run
```


## Features

- User Registration
- User(CRUD)
- User profile updation
- Post(CRUD)
- Follow - Unfollow other users
- Like/Unike Post
- Comments


## Relational Schema
- User(user_id,username,email,password,profile_image,posts,likes,comments,followed)
- Post(post_id, post_title,post_caption,author,posted_by, posted_date,updated_date,comments,likes)
- Like(like_id,author,post_id)
- Cokment(comment_id,comment,author,added_date,post_id)
- followers [Auxilliary table]  which maps followed users to following users
