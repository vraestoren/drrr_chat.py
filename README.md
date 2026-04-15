# <img src="https://github.com/user-attachments/assets/6195de47-f1d4-477f-8f74-84f8741e1af4" width="305" style="vertical-align:middle;" /> drrr_chat.py

> Web-API for [DRRR Chat](https://drrr.chat) an anonymous online chat platform from durarara, dollars forum

## Quick Start

```python
from drrr_chat import DrrrChat

drrr_chat = DrrrChat()
drrr_chat.login(email="you@example.com", password="secret")
```

## Usage

### Authentication

```python
# Login
drrr_chat.login(email="you@example.com", password="secret")

# Register
drrr_chat.register(email="you@example.com", password="secret", username="Hero")

# Forgot password
drrr_chat.forgot_password(email="you@example.com")

# Change email
drrr_chat.change_email(email="new@example.com", password="secret")

# Resend confirmation
drrr_chat.send_confirmation_code(user_id=123)
```

### Discussions

```python
# Browse
drrr_chat.get_discussions()
drrr_chat.get_announcements()
drrr_chat.get_following()

# Create & comment
drrr_chat.create_discussion(title="Hello", content="World", tag_id=20)
drrr_chat.comment_discussion(discussion_id=1, content="Nice post!")

# Read & subscribe
drrr_chat.get_discussion(discussion_id=1)
drrr_chat.follow_discussion(discussion_id=1)
drrr_chat.unfollow_discussion(discussion_id=1)
drrr_chat.ignore_discussion(discussion_id=1)
drrr_chat.mark_all_discussions_read()
```

### Search

```python
drrr_chat.search_discussion(query="hello")
drrr_chat.search_user(query="Hero")
```

### Users

```python
drrr_chat.get_user_info(user_id=123)
drrr_chat.get_user_posts(username="Hero")
drrr_chat.get_user_discussions(username="Hero")
drrr_chat.get_user_mentions(user_id=123)
```

### Notifications

```python
drrr_chat.get_notifications()
```

## API Reference

| Method | Description |
|---|---|
| `login(email, password)` | Login to your account |
| `register(email, password, username)` | Register a new account |
| `forgot_password(email)` | Send a password reset email |
| `change_email(email, password)` | Change your email |
| `send_confirmation_code(user_id)` | Resend confirmation email |
| `get_discussions(offset)` | Get latest discussions |
| `get_announcements(offset)` | Get announcements |
| `get_following(offset)` | Get followed discussions |
| `create_discussion(title, content, tag_id)` | Create a new discussion |
| `get_discussion(discussion_id)` | Get a discussion |
| `comment_discussion(discussion_id, content)` | Post a comment |
| `follow_discussion(discussion_id)` | Follow a discussion |
| `unfollow_discussion(discussion_id)` | Unfollow a discussion |
| `ignore_discussion(discussion_id)` | Ignore a discussion |
| `mark_all_discussions_read()` | Mark all discussions as read |
| `get_notifications()` | Get your notifications |
| `get_user_info(user_id)` | Get a user's profile |
| `get_user_posts(username)` | Get a user's posts |
| `get_user_discussions(username)` | Get a user's discussions |
| `get_user_mentions(user_id)` | Get posts mentioning a user |
| `search_discussion(query)` | Search discussions |
| `search_user(query)` | Search users |
