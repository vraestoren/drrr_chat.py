from datetime import datetime
from requests import Session, Response

class DrrrChat:
	def __init__(self) -> None:
		self.api = "https://drrr.chat"
		self.session = Session()
		self.session.headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}
		self.token = None
		self.user_id = None
		self.get_cookies()


	def _post(self, endpoint: str, data: dict = None) -> Response:
		return self.session.post(f"{self.api}{endpoint}", data=data)

	def _get(
			self, endpoint: str, params: dict = {}) -> dict:
		return self.session.get(endpoint, params=params).json()

	def get_cookies(self) -> None:
		response = self._get(self.api)
		self.flarum_session = response.cookies["flarum_session"]
		self.csrf_token = response.headers["X-CSRF-Token"]
		self.session.headers["cookie"] = f"flarum_session={self.flarum_session}"
		self.session.headers["X-Csrf-Token"] = self.csrf_token
		
	def login(
			self,
			email: str,
			password: str,
			remember: bool = True) -> dict:
		data = {
			"identification": email,
			"password": password,
			"remember": remember
		}
		response = self._post("/login", data=data)
		content = response.json()
		cookies = response.cookies
		if "token" in content:
			self.token = content["token"]
			self.user_id = content["userId"]
			self.flarum_session = cookies["flarum_session"]
			self.flarum_remember = cookies["flarum_remember"]
			self.session.headers["x-csrf-token"] = self.csrf_token
			self.session.headers["cookie"] = f"flarum_remember={self.flarum_remember}; flarum_session={self.flarum_session}"
		return content

	def register(
			self,
			email: str,
			password: str,
			username: str) -> dict:
		data = {
			"email": email,
			"password": password,
			"username": username
		}
		return self._post("/register", data).json()

	def send_confirmation_code(self, user_id: int) -> dict:
		return self._post("/api/users/{user_id}/send-confirmation").json()

	def forgot_password(self, email: str) -> dict:
		data = {
			"email": email
		}
		return self._post("/api/forgot", data).json()

	def change_email(
			self,
			email: str,
			password: str) -> dict:
		data = {
			"data": {
				"type": "users",
				"id": self.user_id,
				"attributes": {"email": email}
			},
			"meta": {
				"password": password
			}
		}
		return self._post(f"/api/users/{self.user_id}", data).json()

	def get_discussions(
			self,
			offset: int = 0,
			include: str = "user,lastPostedUser,tags,tags.parent,firstPost") -> dict:
		params = {
			"include": include,
			"page[offset]": offset
		}
		return self._get(f"{self.api}/api/discussions", params)

	def get_announcements(
			self,
			offset: int = 0,
			include: str = "user,lastPostedUser,tags,tags.parent,firstPost",
			tag: str = "announcement") -> dict:
		params = {
			"include": include,
			"filter[tag]": tag,
			"page[offset]": offset
		}
		return self._get(f"{self.api}/api/discussions", params)

	def get_following(
			self,
			offset: int = 0,
			include: str = "user,lastPostedUser,tags,tags.parent,firstPost") -> dict:
		params = {
			"include": include,
			"page[offset]": offset,
			"filter[subscription]": "following"
		}
		return self._get(f"{self.api}/api/discussions", params)

	def create_discussion(
			self,
			title: str, 
			content: str, 
			tag_id: int = 20) -> dict:
		data = {
			"data": {
				"type": "discussions", 
				"attributes": {
					"title": title,
					"content": content
				},
				"relationships": {
					"tags": {
						"data": [
							{
								"type": "tags", 
								"id": tag_id
							}
						]
					}
				}
			}
		}
		return self._post("/api/discussions", data).json()
	
	def get_notifications(self) -> dict:
		return self._get(f"{self.api}/api/notifications")

	def get_discussion(
			self,
			discussion_id: int,
			last_read_post_number: int = 1) -> dict:
		data = {
			"data": {
				"type": "discussions",
				"attributes": {
					"lastReadPostNumber": last_read_post_number
				},
				"id": discussion_id
			}
		}
		return self._post(f"/api/discussions/{discussion_id}", data).json()

	def follow_discussion(self, discussion_id: int) -> dict:
		data = {
			"data": {
				"type": "discussions",
				"attributes": {
					"subscription": "follow"
				},
				"id": discussion_id
			}
		}
		return self._post(f"/api/discussions/{discussion_id}", data).json()

	def unfollow_discussion(self, discussion_id: int) -> dict:
		data = {
			"data": {
				"type": "discussions",
				"attributes": {
					"subscription": None
				},
				"id": discussion_id
			}
		}
		return self._post(f"/api/discussions/{discussion_id}", data).json()

	def ignore_discussion(self, discussion_id: int) -> dict:
		data = {
			"data": {
				"type": "discussions",
				"attributes": {
					"subscription": "ignore"
				},
				"id": discussion_id
			}
		}
		return self._post(f"/api/discussions/{discussion_id}", data).json()

	def get_user_posts(
			self,
			username: str,
			type: str = "comment",
			offset: int = 20,
			limit: int = 20,
			sort: str = "-createdAt") -> dict:
		params = {
			"filter[author]": username,
			"filter[type]": type,
			"page[offset]": offset,
			"page[limit]": limit,
			"sort": sort
		}
		return self._get(f"{self.api}/api/posts", params)

	def get_user_discussions(
			self,
			username: str,
			include: str = "user,lastPostedUser,tags,tags.parent",
			sort: str = "-createdAt",
			offset: int = 0) -> dict:
		params = {
			"include": include,
			"filter[author]": username,
			"sort": sort,
			"page[offset]": offset
		}
		return self._get(f"{self.api}/api/discussions", params)

	def get_user_mentions(
			self,
			user_id: int,
			type: str = "comment",
			offset: int = 20,
			limit: int = 20,
			sort: str = "-createdAt") -> dict:
		params = {
			"filter[type]": type,
			"filter[mentioned]": user_id,
			"page[offset]": offset,
			"page[limit]": limit,
			"sort": sort
		}
		return self._get(f"{self.api}/api/posts", params)

	def get_user_info(self, user_id: int) -> dict:
		return self._get(f"{self.api}/api/users/{user_id}")

	def comment_discussion(
			self,
			discussion_id: int,
			content: str) -> dict:
		data = {
			"data": {
				"type": "posts",
				"attributes": {
					"content": content
				},
				"relationships": {
					"discussion": {
						"data": {
							"type": "discussions",
							"id": discussion_id
						}
					}
				}
			}
		}
		return self._post("/api/posts", data).json()

	def search_user(self, query: str, limit: int = 5) -> dict:
		params = {
			"filter[q]": query,
			"page[limit]": limit
		}
		return self._get(f"{self.api}/api/users", params)

	def search_discussion(
			self,
			query: str,
			limit: int = 5,
			include: str = "mostRelevantPost") -> dict:
		params = {
			"filter[q]": query,
			"page[limit]": limit,
			"include": include
		}
		return self._get(f"{self.api}/api/discussions", params)

	def mark_all_discussions_read(self) -> dict:
		data = {
			"data": {
				"type": "users",
				"attributes": {
					"markedAllAsReadAt": f"{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z"
				},
				"id": self.user_id
			}
		}
		return self._post(f"/api/users/{user_id}", data).json()
