from locust import HttpUser, task, between
import csv

# 載入所有使用者資料（一次載入記憶體）
users = []
with open("user.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        users.append(row)



class WebsiteUser(HttpUser):
    wait_time = between(1, 2)  # 每個使用者行為的等待時間

    def on_start(self):
        # 每位使用者啟動時先登入取得 token

        user = users[self.environment.runner.user_count % len(users)]

        self.user_id = user["userid"]

        res = self.client.post("/api/user/special_login", json={
            "key" : "DqjGwVF0jezFxbzt8Co1c0xQIz71gpbFftCpmgg4mq5UMJZSdFcYgoL26kd4tmra",
            "user_id" : self.user_id
        })
        self.token = res.json().get("data", {}).get("token")

    @task
    def call_main_api(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.post("/api/board/overall/monthly", json={"month": "2025-07"}, headers=headers)

