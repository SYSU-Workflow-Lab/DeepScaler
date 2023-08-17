from locust import HttpUser, TaskSet, task, constant
from locust import LoadTestShape
import random
from random import randint, choice
import base64
from atomic_queries import _query_advanced_ticket, _login
import time
# from query_advanced_ticket import kk
import json
from typing import List
import random
from typing import List
import string
import logging
import random
import time


class TrainTicketUserTasks(TaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        
        
####工具
    def random_boolean(self) -> bool:
        return random.choice([True, False])

    def random_from_list(self,l: List):
        return random.choice(l)

    def random_from_weighted(self,d: dict):
        """
        :param d: 带相对权重的字典，eg. {'a': 100, 'b': 50}
        :return: 返回随机选择的key
        """
        total = sum(d.values())    # 权重求和
        ra = random.uniform(0, total)   # 在0与权重和之前获取一个随机数
        curr_sum = 0
        ret = None

        keys = d.keys()
        for k in keys:
            curr_sum += d[k]             # 在遍历中，累加当前权重值
            if ra <= curr_sum:          # 当随机数<=当前权重和时，返回权重key
                ret = k
                break

        return ret


    def random_str(self):
        ''.join(random.choices(string.ascii_letters, k=random.randint(4, 10)))


    def random_phone(self):
        ''.join(random.choices(string.digits, k=random.randint(8, 15)))
    

    logger = logging.getLogger("query_and_preserve")
    uuid = "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f"
    date = time.strftime("%Y-%m-%d", time.localtime())
    def random_boolean(self) -> bool:
        return random.choice([True, False])
    ##   1     ######################################################################################################################
    # @task(1)
    # def index(self):
    #     self.client.get("/")
    ##   2     ######################################################################################################################
    #@task(1)
    def login(self):
        username="fdse_microservice"
        password="111111"
        url = f"/api/v1/users/login"
        
        cookies = {
            'JSESSIONID': '9ED5635A2A892A4BA31E7E98533A279D',
            'YsbCaptcha': '025080CF8BA94594B09E283F17815444',
        }
            # 'Origin': url,
            # 'Referer': f"/client_login.html",
            # 'Proxy-Connection': 'keep-alive',
            # 'Connection': 'close'
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Content-Type': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

        data = '{"username":"' + username + '","password":"' + password + '"}'
        r = self.client.post(url=url, headers=headers,
                        cookies=cookies, data=data, verify=False)
        #print(r.status_code)
        if r.status_code == 200:
            data = r.json().get("data")
            uid = data.get("userId")
            token = data.get("token")
            return uid, token
        return None, None

    # ##   3     ######################################################################################################################
    @task(1)
    def query_admin_basic_config_use(self):
        _, token = self.login()
        headers = {
            "Cookie": "JSESSIONID=823B2652E3F5B64A1C94C924A05D80AF; YsbCaptcha=2E037F4AB09D49FA9EE3BE4E737EAFD2",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZHNlX21pY3Jvc2VydmljZSIsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJpZCI6IjRkMmE0NmM3LTcxY2ItNGNmMS1iNWJiLWI2ODQwNmQ5ZGE2ZiIsImlhdCI6MTYyNzE5OTA0NCwiZXhwIjoxNjI3MjAyNjQ0fQ.3IIwwz7AwqHtOFDeXfih25i6_7nQBPL_K7BFxuyFiKQ",
            "Content-Type": "application/json"
        }
        headers["Authorization"] = "Bearer " + token
        
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.query_admin_basic_config(headers=headers)
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"start:{start_time} end:{end_time}")
 
      ##############5     ######################################################################################################################               
    @task(1)
    def query_advanced_ticket_use(self):
        _, token = self.login()
        headers = {
            "Cookie": "JSESSIONID=823B2652E3F5B64A1C94C924A05D80AF; YsbCaptcha=2E037F4AB09D49FA9EE3BE4E737EAFD2",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZHNlX21pY3Jvc2VydmljZSIsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJpZCI6IjRkMmE0NmM3LTcxY2ItNGNmMS1iNWJiLWI2ODQwNmQ5ZGE2ZiIsImlhdCI6MTYyNzE5OTA0NCwiZXhwIjoxNjI3MjAyNjQ0fQ.3IIwwz7AwqHtOFDeXfih25i6_7nQBPL_K7BFxuyFiKQ",
            "Content-Type": "application/json"
        }
        headers["Authorization"] = "Bearer " + token
        place_pairs = [("Shang Hai", "Su Zhou"),
                    ("Su Zhou", "Shang Hai"),
                    ("Nan Jing", "Shang Hai")]
        type = "quickest"
        url = f"/api/v1/travelplanservice/travelPlan/" + type
        place_pair = random.choice(place_pairs)
        
        payload = {
            "departureTime": time.strftime("%Y-%m-%d", time.localtime()),
            "startingPlace": place_pair[0],
            "endPlace": place_pair[1],
        }
        
        self.client.post(url, headers=headers, json=payload)
    
      ###################6     ######################################################################################################################
    @task(1)        
    def query_and_preserve_use(self):
        _, token = self.login()
        headers = {
            "Cookie": "JSESSIONID=823B2652E3F5B64A1C94C924A05D80AF; YsbCaptcha=2E037F4AB09D49FA9EE3BE4E737EAFD2",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZHNlX21pY3Jvc2VydmljZSIsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJpZCI6IjRkMmE0NmM3LTcxY2ItNGNmMS1iNWJiLWI2ODQwNmQ5ZGE2ZiIsImlhdCI6MTYyNzE5OTA0NCwiZXhwIjoxNjI3MjAyNjQ0fQ.3IIwwz7AwqHtOFDeXfih25i6_7nQBPL_K7BFxuyFiKQ",
            "Content-Type": "application/json"
        }
        headers["Authorization"] = "Bearer " + token
        """
        1. 查票（随机高铁或普通）
        2. 查保险、Food、Contacts
        3. 随机选择Contacts、保险、是否买食物、是否托运
        4. 买票
        :return:
        """
        start = ""
        end = ""
        trip_ids = []
        PRESERVE_URL = ""

        high_speed = self.random_boolean()
        if high_speed:
            start = "Shang Hai"
            end = "Su Zhou"
            high_speed_place_pair = (start, end)
            trip_ids = self.query_high_speed_ticket(place_pair=high_speed_place_pair, headers=headers, time=time.strftime("%Y-%m-%d", time.localtime()))
            PRESERVE_URL = f"/api/v1/preserveservice/preserve"
        else:
            start = "Shang Hai"
            end = "Nan Jing"
            other_place_pair = (start, end)
            trip_ids = self.query_normal_ticket(place_pair=other_place_pair, headers=headers, time=time.strftime("%Y-%m-%d", time.localtime()))
            PRESERVE_URL = f"/api/v1/preserveotherservice/preserveOther"

        _ = self.query_assurances(headers=headers)
        food_result = self.query_food(headers=headers)
        contacts_result = self.query_contacts(headers=headers)

        base_preserve_payload = {
            "accountId": self.uuid,
            "assurance": "0",
            "contactsId": "",
            "date": time.strftime("%Y-%m-%d", time.localtime()),
            "from": start,
            "to": end,
            "tripId": ""
        }

        trip_id = self.random_from_list(trip_ids)
        base_preserve_payload["tripId"] = trip_id

        need_food = self.random_boolean()
        if need_food:
            self.logger.info("need food")
            food_dict = self.random_from_list(food_result)
            base_preserve_payload.update(food_dict)
        else:
            self.logger.info("not need food")
            base_preserve_payload["foodType"] = "0"

        need_assurance = self.random_boolean()
        if need_assurance:
            base_preserve_payload["assurance"] = 1

        contacts_id = self.random_from_list(contacts_result)
        base_preserve_payload["contactsId"] = contacts_id

        # 高铁 2-3
        seat_type = self.random_from_list(["2", "3"])
        base_preserve_payload["seatType"] = seat_type

        need_consign = self.random_boolean()
        if need_consign:
            consign = {
                "consigneeName": self.random_str(),
                "consigneePhone": self.random_phone(),
                "consigneeWeight": random.randint(1, 10),
                "handleDate": time.strftime("%Y-%m-%d", time.localtime())
            }
            base_preserve_payload.update(consign)

        print("payload:" + str(base_preserve_payload))

        print(f"choices: preserve_high: {high_speed} need_food:{need_food}  need_consign: {need_consign}  need_assurance:{need_assurance}")

        res = self.client.post(url=PRESERVE_URL,
                            headers=headers,
                            json=base_preserve_payload)

        print(res.json())
        if res.json()["data"] != "Success":
            raise Exception(res.json() + " not success")
        print()
        
    #   7     ######################################################################################################################    
    @task(1)
    def query_admin_basic_price_use(self):   
        _, token = self.login()
        headers = {
            "Cookie": "JSESSIONID=823B2652E3F5B64A1C94C924A05D80AF; YsbCaptcha=2E037F4AB09D49FA9EE3BE4E737EAFD2",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZHNlX21pY3Jvc2VydmljZSIsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJpZCI6IjRkMmE0NmM3LTcxY2ItNGNmMS1iNWJiLWI2ODQwNmQ5ZGE2ZiIsImlhdCI6MTYyNzE5OTA0NCwiZXhwIjoxNjI3MjAyNjQ0fQ.3IIwwz7AwqHtOFDeXfih25i6_7nQBPL_K7BFxuyFiKQ",
            "Content-Type": "application/json"
        }
        headers["Authorization"] = "Bearer " + token
        
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.query_admin_basic_price(headers=headers)
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"start:{start_time} end:{end_time}")

    ##   8     ######################################################################################################################    
    @task(1)
    def query_and_cancel_use(self):
        _, token = self.login()
        headers = {
            "Cookie": "JSESSIONID=823B2652E3F5B64A1C94C924A05D80AF; YsbCaptcha=2E037F4AB09D49FA9EE3BE4E737EAFD2",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZHNlX21pY3Jvc2VydmljZSIsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJpZCI6IjRkMmE0NmM3LTcxY2ItNGNmMS1iNWJiLWI2ODQwNmQ5ZGE2ZiIsImlhdCI6MTYyNzE5OTA0NCwiZXhwIjoxNjI3MjAyNjQ0fQ.3IIwwz7AwqHtOFDeXfih25i6_7nQBPL_K7BFxuyFiKQ",
            "Content-Type": "application/json"
        }
        headers["Authorization"] = "Bearer " + token
        #uuid = "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f"

        self.query_one_and_cancel(headers=headers,uuid=self.uuid,)               
    # #   9     ######################################################################################################################    
    @task(1)
    def query_and_collect_ticket_use(self): 
        _, token = self.login()
        headers = {
            "Cookie": "JSESSIONID=823B2652E3F5B64A1C94C924A05D80AF; YsbCaptcha=2E037F4AB09D49FA9EE3BE4E737EAFD2",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZHNlX21pY3Jvc2VydmljZSIsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJpZCI6IjRkMmE0NmM3LTcxY2ItNGNmMS1iNWJiLWI2ODQwNmQ5ZGE2ZiIsImlhdCI6MTYyNzE5OTA0NCwiZXhwIjoxNjI3MjAyNjQ0fQ.3IIwwz7AwqHtOFDeXfih25i6_7nQBPL_K7BFxuyFiKQ",
            "Content-Type": "application/json"
        }
        headers["Authorization"] = "Bearer " + token
        self.query_and_collect_ticket(headers=headers)      

    #   10     ######################################################################################################################    
    @task(1)    
    def query_and_enter_station_use(self):
        _, token = self.login()
        headers = {
            "Cookie": "JSESSIONID=823B2652E3F5B64A1C94C924A05D80AF; YsbCaptcha=2E037F4AB09D49FA9EE3BE4E737EAFD2",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZHNlX21pY3Jvc2VydmljZSIsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJpZCI6IjRkMmE0NmM3LTcxY2ItNGNmMS1iNWJiLWI2ODQwNmQ5ZGE2ZiIsImlhdCI6MTYyNzE5OTA0NCwiZXhwIjoxNjI3MjAyNjQ0fQ.3IIwwz7AwqHtOFDeXfih25i6_7nQBPL_K7BFxuyFiKQ",
            "Content-Type": "application/json"
        }
        headers["Authorization"] = "Bearer " + token
        self.query_and_enter_station(headers=headers)

    #   11     ######################################################################################################################    
    @task(1)
    def query_and_put_consign_use(self):
        _, token = self.login()
        headers = {
            "Cookie": "JSESSIONID=823B2652E3F5B64A1C94C924A05D80AF; YsbCaptcha=2E037F4AB09D49FA9EE3BE4E737EAFD2",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZHNlX21pY3Jvc2VydmljZSIsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJpZCI6IjRkMmE0NmM3LTcxY2ItNGNmMS1iNWJiLWI2ODQwNmQ5ZGE2ZiIsImlhdCI6MTYyNzE5OTA0NCwiZXhwIjoxNjI3MjAyNjQ0fQ.3IIwwz7AwqHtOFDeXfih25i6_7nQBPL_K7BFxuyFiKQ",
            "Content-Type": "application/json"
        }
        headers["Authorization"] = "Bearer " + token
        uuid = "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f"

        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        pairs = self.query_orders_all_info(headers=headers)
        pairs2 = self.query_orders_all_info(headers=headers, query_other=True)
        pairs = pairs + pairs2
        self.query_one_and_put_consign(headers=headers, pairs=pairs)
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        print(f"start:{start_time} end:{end_time}")
    # ##   12     ######################################################################################################################    
    @task(1)
    def query_and_rebook_use(self):
        _, token = self.login()
        headers = {
            "Cookie": "JSESSIONID=823B2652E3F5B64A1C94C924A05D80AF; YsbCaptcha=2E037F4AB09D49FA9EE3BE4E737EAFD2",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZHNlX21pY3Jvc2VydmljZSIsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJpZCI6IjRkMmE0NmM3LTcxY2ItNGNmMS1iNWJiLWI2ODQwNmQ5ZGE2ZiIsImlhdCI6MTYyNzE5OTA0NCwiZXhwIjoxNjI3MjAyNjQ0fQ.3IIwwz7AwqHtOFDeXfih25i6_7nQBPL_K7BFxuyFiKQ",
            "Content-Type": "application/json"
        }
        headers["Authorization"] = "Bearer " + token
        
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.query_and_rebook(headers=headers)

        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        print(f"start:{start_time} end:{end_time}")    
        
    ##   13     ######################################################################################################################    
    @task(1)
    def query_food_use(self):       
        _, token = self.login()
        headers = {
            "Cookie": "JSESSIONID=823B2652E3F5B64A1C94C924A05D80AF; YsbCaptcha=2E037F4AB09D49FA9EE3BE4E737EAFD2",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZHNlX21pY3Jvc2VydmljZSIsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJpZCI6IjRkMmE0NmM3LTcxY2ItNGNmMS1iNWJiLWI2ODQwNmQ5ZGE2ZiIsImlhdCI6MTYyNzE5OTA0NCwiZXhwIjoxNjI3MjAyNjQ0fQ.3IIwwz7AwqHtOFDeXfih25i6_7nQBPL_K7BFxuyFiKQ",
            "Content-Type": "application/json"
        }
        headers["Authorization"] = "Bearer " + token       
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self.query_food(headers=headers)
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        print(f"start:{start_time} end:{end_time}")
    #   14     ######################################################################################################################    
    @task(1)
    def query_order_and_pay_use(self):       
        _, token = self.login()
        headers = {
            "Cookie": "JSESSIONID=823B2652E3F5B64A1C94C924A05D80AF; YsbCaptcha=2E037F4AB09D49FA9EE3BE4E737EAFD2",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZHNlX21pY3Jvc2VydmljZSIsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJpZCI6IjRkMmE0NmM3LTcxY2ItNGNmMS1iNWJiLWI2ODQwNmQ5ZGE2ZiIsImlhdCI6MTYyNzE5OTA0NCwiZXhwIjoxNjI3MjAyNjQ0fQ.3IIwwz7AwqHtOFDeXfih25i6_7nQBPL_K7BFxuyFiKQ",
            "Content-Type": "application/json"
        }
        headers["Authorization"] = "Bearer " + token              
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        pairs = self.query_orders(headers=headers, types=tuple([0, 1]))
        pairs2 = self.query_orders(headers=headers, types=tuple([0, 1]), query_other=True)

        pairs = pairs + pairs2

        for i in range(330):
            try:
                self.query_order_and_pay(headers=headers, pairs=pairs)
                print("*****************************INDEX:" + str(i))
            except Exception as e:
                print(e)

        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        print(f"start:{start_time} end:{end_time}")        
    ##   15     ######################################################################################################################    
    @task(1)
    def query_route_use(self):        
        _, token = self.login()
        headers = {
            "Cookie": "JSESSIONID=823B2652E3F5B64A1C94C924A05D80AF; YsbCaptcha=2E037F4AB09D49FA9EE3BE4E737EAFD2",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZHNlX21pY3Jvc2VydmljZSIsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJpZCI6IjRkMmE0NmM3LTcxY2ItNGNmMS1iNWJiLWI2ODQwNmQ5ZGE2ZiIsImlhdCI6MTYyNzE5OTA0NCwiZXhwIjoxNjI3MjAyNjQ0fQ.3IIwwz7AwqHtOFDeXfih25i6_7nQBPL_K7BFxuyFiKQ",
            "Content-Type": "application/json"
        }
        headers["Authorization"] = "Bearer " + token
        self.query_route(headers=headers)     
    # ##   16     ######################################################################################################################    
    @task(1)
    def query_travel_left_parallel_use(self):
        _, token = self.login()
        headers = {
            "Cookie": "JSESSIONID=823B2652E3F5B64A1C94C924A05D80AF; YsbCaptcha=2E037F4AB09D49FA9EE3BE4E737EAFD2",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZHNlX21pY3Jvc2VydmljZSIsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJpZCI6IjRkMmE0NmM3LTcxY2ItNGNmMS1iNWJiLWI2ODQwNmQ5ZGE2ZiIsImlhdCI6MTYyNzE5OTA0NCwiZXhwIjoxNjI3MjAyNjQ0fQ.3IIwwz7AwqHtOFDeXfih25i6_7nQBPL_K7BFxuyFiKQ",
            "Content-Type": "application/json"
        }
        headers["Authorization"] = "Bearer " + token

        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"start:{start_time}")
        self.query_travel_left_parallel(headers=headers)
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        print(f"start:{start_time} end:{end_time}")

    ##   17     ######################################################################################################################    
    @task(1)
    def query_travel_left_use(self):
        _, token = self.login()
        headers = {
            "Cookie": "JSESSIONID=823B2652E3F5B64A1C94C924A05D80AF; YsbCaptcha=2E037F4AB09D49FA9EE3BE4E737EAFD2",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZHNlX21pY3Jvc2VydmljZSIsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJpZCI6IjRkMmE0NmM3LTcxY2ItNGNmMS1iNWJiLWI2ODQwNmQ5ZGE2ZiIsImlhdCI6MTYyNzE5OTA0NCwiZXhwIjoxNjI3MjAyNjQ0fQ.3IIwwz7AwqHtOFDeXfih25i6_7nQBPL_K7BFxuyFiKQ",
            "Content-Type": "application/json"
        }
        headers["Authorization"] = "Bearer " + token
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"start:{start_time}")


        self.query_travel_left(headers=headers)
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        print(f"start:{start_time} end:{end_time}")




                       
    def query_high_speed_ticket(self,place_pair: tuple = ("Shang Hai", "Su Zhou"), headers: dict = {},
                                time: str = "2021-07-15") -> List[str]:
        """
        返回TripId 列表
        :param place_pair: 使用的开始结束组对
        :param headers: 请求头
        :return: TripId 列表
        """

        url = f"/api/v1/travelservice/trips/left"
        place_pairs = [("Shang Hai", "Su Zhou"),
                    ("Su Zhou", "Shang Hai"),
                    ("Nan Jing", "Shang Hai")]

        payload = {
            "departureTime": time,
            "startingPlace": place_pair[0],
            "endPlace": place_pair[1],
        }

        response = self.client.post(url=url,
                                headers=headers,
                                json=payload)

        if response.status_code is not 200 or response.json().get("data") is None:
            self.logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        data = response.json().get("data")  # type: dict

        trip_ids = []
        for d in data:
            trip_id = d.get("tripId").get("type") + d.get("tripId").get("number")
            trip_ids.append(trip_id)
        return trip_ids

    def query_normal_ticket(self,place_pair: tuple = ("Nan Jing", "Shang Hai"), headers: dict = {},
                            time: str = "2021-07-15") -> List[str]:
        url = f"/api/v1/travel2service/trips/left"
        place_pairs = [("Shang Hai", "Nan Jing"),
                    ("Nan Jing", "Shang Hai")]

        payload = {
            "departureTime": time,
            "startingPlace": place_pair[0],
            "endPlace": place_pair[1],
        }

        response = self.client.post(url=url,
                                headers=headers,
                                json=payload)
        if response.status_code is not 200 or response.json().get("data") is None:
            self.logger.warning(f"request for {url} failed. response data is {response.json()}")
            return None

        data = response.json().get("data")  # type: dict

        trip_ids = []
        for d in data:
            trip_id = d.get("tripId").get("type") + d.get("tripId").get("number")
            trip_ids.append(trip_id)
        return trip_ids        

    def query_assurances(self,headers: dict = {}):
        url = f"/api/v1/assuranceservice/assurances/types"
        response = self.client.get(url=url, headers=headers)
        if response.status_code is not 200 or response.json().get("data") is None:
            self.self.logger.warning(f"query assurance failed, response data is {response.json()}")
            return None
        data = response.json().get("data")
        # assurance只有一种

        return [{"assurance": "1"}]
    
    def query_food(self,place_pair: tuple = ("Shang Hai", "Su Zhou"), train_num: str = "D1345", headers: dict = {}):
        url = f"/api/v1/foodservice/foods/2021-07-14/{place_pair[0]}/{place_pair[1]}/{train_num}"

        response = self.client.get(url=url, headers=headers)
        if response.status_code is not 200 or response.json().get("data") is None:
            self.logger.warning(f"query food failed, response data is {response}")
            return None
        data = response.json().get("data")

        # food 是什么不会对后续调用链有影响，因此查询后返回一个固定数值
        return [{
            "foodName": "Soup",
            "foodPrice": 3.7,
            "foodType": 2,
            "stationName": "Su Zhou",
            "storeName": "Roman Holiday"
        }]


    def query_contacts(self,headers: dict = {}) -> List[str]:
        """
        返回座位id列表
        :param headers:
        :return: id list
        """
        url = f"/api/v1/contactservice/contacts/account/{self.uuid}"
        response = self.client.get(url=url, headers=headers)
        if response.status_code is not 200 or response.json().get("data") is None:
            self.logger.warning(f"query contacts failed, response data is {response.json()}")
            return None

        data = response.json().get("data")
        # print("contacts")
        # pprint(data)

        ids = [d.get("id") for d in data if d.get("id") is not None]
        # pprint(ids)
        return ids
 
    def query_admin_basic_config(self,headers: dict = {}):
        url = f"/api/v1/adminbasicservice/adminbasic/configs"
        response = self.client.get(url=url,headers=headers)
        if response.status_code == 200:
            print(f"config success")
            return response
        else:
            print(f"config failed")
            return None   



    def admin_login(self):
        return self.login()


    def query_high_speed_ticket_parallel(self,place_pair: tuple = ("Shang Hai", "Su Zhou"), headers: dict = {},
                                        time: str = "2021-07-15") -> List[str]:
        """
        返回TripId 列表
        :param place_pair: 使用的开始结束组对
        :param headers: 请求头
        :return: TripId 列表
        """

        url = f"/api/v1/travelservice/trips/left_parallel"
        place_pairs = [("Shang Hai", "Su Zhou"),
                    ("Su Zhou", "Shang Hai"),
                    ("Nan Jing", "Shang Hai")]

        payload = {
            "departureTime": time,
            "startingPlace": place_pair[0],
            "endPlace": place_pair[1],
        }

        response = self.client.post(url=url,
                                headers=headers,
                                json=payload)
        print(response.status_code)
        if response.status_code is not 200 or response.json().get("data") is None:
            self.logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        data = response.json().get("data")  # type: dict

        trip_ids = []
        for d in data:
            trip_id = d.get("tripId").get("type") + d.get("tripId").get("number")
            trip_ids.append(trip_id)
        return trip_ids


    def query_advanced_ticket(self,place_pair: tuple = ("Nan Jing", "Shang Hai"), headers: dict = {}, time: str = "2021-07-15",
                            type: str = "cheapest") -> List[str]:
        url = f"/api/v1/travelplanservice/travelPlan/" + type
        print(url)

        payload = {
            "departureTime": time,
            "startingPlace": place_pair[0],
            "endPlace": place_pair[1],
        }

        # print(payload)

        response = self.client.post(url=url,
                                headers=headers,
                                json=payload)
        # print(response.text)
        if response.status_code is not 200 or response.json().get("data") is None:
            self.logger.warning(f"request for {url} failed. response data is {response.json()}")
            return None

        data = response.json().get("data")

        trip_ids = []
        for d in data:
            trip_id = d.get("tripId")
            trip_ids.append(trip_id)
        return trip_ids


    def query_orders(self,headers: dict = {}, types: tuple = tuple([0]), query_other: bool = False) -> List[tuple]:
        """
        返回(orderId, tripId) triple list for inside_pay_service
        :param headers:
        :return:
        """
        url = ""

        if query_other:
            url = f"/api/v1/orderOtherService/orderOther/refresh"
        else:
            url = f"/api/v1/orderservice/order/refresh"

        payload = {
            "loginId": self.uuid,
        }

        response = self.client.post(url=url, headers=headers, json=payload)
        if response.status_code is not 200 or response.json().get("data") is None:
            self.logger.warning(f"query orders failed, response data is {response.text}")
            return None

        data = response.json().get("data")
        pairs = []
        for d in data:
            # status = 0: not paid
            # status=1 paid not collect
            # status=2 collected
            print(types)
            print(d.get("status"))
            if d.get("status") in types:
                order_id = d.get("id")
                trip_id = d.get("trainNumber")
                pairs.append((order_id, trip_id))
        print(f"queried {len(pairs)} orders")

        return pairs


    def query_orders_all_info(self,headers: dict = {}, query_other: bool = False) -> List[tuple]:
        """
        返回(orderId, tripId) triple list for consign service
        :param headers:
        :return:
        """

        if query_other:
            url = f"/api/v1/orderOtherService/orderOther/refresh"
        else:
            url = f"/api/v1/orderservice/order/refresh"

        payload = {
            "loginId": self.uuid,
        }

        response = self.client.post(url=url, headers=headers, json=payload)
        if response.status_code is not 200 or response.json().get("data") is None:
            self.logger.warning(f"query orders failed, response data is {response.text}")
            return None

        data = response.json().get("data")
        pairs = []
        for d in data:
            result = {}
            result["accountId"] = d.get("accountId")
            result["targetDate"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            result["orderId"] = d.get("id")
            result["from"] = d.get("from")
            result["to"] = d.get("to")
            pairs.append(result)
        print(f"queried {len(pairs)} orders")

        return pairs


    def put_consign(self,result, headers: dict = {}):
        url = f"/api/v1/consignservice/consigns"
        consignload = {
            "accountId": result["accountId"],
            "handleDate": time.strftime('%Y-%m-%d', time.localtime(time.time())),
            "targetDate": result["targetDate"],
            "from": result["from"],
            "to": result["to"],
            "orderId": result["orderId"],
            "consignee": "32",
            "phone": "12345677654",
            "weight": "32",
            "id": "",
            "isWithin": False
        }
        response = self.client.put(url=url, headers=headers,
                                json=consignload)

        order_id = result["orderId"]
        if response.status_code == 200 or response.status_code == 201:
            print(f"{order_id} put consign success")
        else:
            print(f"{order_id} failed!")
            return None

        return order_id


    def query_route(self,routeId: str = '92708982-77af-4318-be25-57ccb0ff69ad', headers: dict = {}):
        url = f"/api/v1/routeservice/routes/{routeId}"

        res = self.client.get(url=url, headers=headers)

        if res.status_code == 200:
            print(f"query {routeId} success")
        else:
            print(f"query {routeId} fail")

        return


    def pay_one_order(self,order_id, trip_id, headers: dict = {}):
        url = f"/api/v1/inside_pay_service/inside_payment"
        payload = {
            "orderId": order_id,
            "tripId": trip_id
        }

        response = self.client.post(url=url, headers=headers,
                                json=payload)

        if response.status_code == 200:
            print(f"{order_id} pay success")
        else:
            print(f"pay {order_id} failed!")
            return None

        return order_id


    def cancel_one_order(self,order_id, uuid, headers: dict = {}):
        print("orderid  ssj")
        print(order_id)
        print("uuid")
        print(uuid)
        url = f"/api/v1/cancelservice/cancel/{order_id}/{uuid}"
        print(url)
        response = self.client.get(url=url,
                                headers=headers)

        if response.status_code == 200:
            print(f"{order_id} cancel success")
        else:
            print(f"{order_id} cancel failed")

        return order_id


    def collect_one_order(self,order_id, headers: dict = {}):
        url = f"/api/v1/executeservice/execute/collected/{order_id}"
        response = self.client.get(url=url,
                                headers=headers)
        if response.status_code == 200:
            print(f"{order_id} collect success")
        else:
            print(f"{order_id} collect failed")

        return order_id


    def enter_station(self,order_id, headers: dict = {}):
        url = f"/api/v1/executeservice/execute/execute/{order_id}"
        response = self.client.get(url=url,
                                headers=headers)
        if response.status_code == 200:
            print(f"{order_id} enter station success")
        else:
            print(f"{order_id} enter station failed")

        return order_id


    def query_cheapest(self,date="2021-12-31", headers: dict = {}):
        url = f"/api/v1/travelplanservice/travelPlan/cheapest"

        payload = {
            "departureTime": date,
            "endPlace": "Shang Hai",
            "startingPlace": "Nan Jing"
        }

        r = self.client.post(url=url, json=payload, headers=headers)
        if r.status_code == 200:
            print("query cheapest success")
        else:
            print("query cheapest failed")


    def query_min_station(self,date="2021-12-31", headers: dict = {}):
        url = f"/api/v1/travelplanservice/travelPlan/minStation"

        payload = {
            "departureTime": date,
            "endPlace": "Shang Hai",
            "startingPlace": "Nan Jing"
        }

        r = self.client.post(url=url, json=payload, headers=headers)
        if r.status_code == 200:
            print("query min station success")
        else:
            print("query min station failed")


    def query_quickest(self,date="2021-12-31", headers: dict = {}):
        url = f"/api/v1/travelplanservice/travelPlan/quickest"

        payload = {
            "departureTime": date,
            "endPlace": "Shang Hai",
            "startingPlace": "Nan Jing"
        }

        r = self.client.post(url=url, json=payload, headers=headers)
        if r.status_code == 200:
            print("query quickest success")
        else:
            print("query quickest failed")


    def query_admin_basic_price(self,headers: dict = {}):
        url = f"/api/v1/adminbasicservice/adminbasic/prices"
        response = self.client.get(url=url,
                                headers=headers)
        if response.status_code == 200:
            print(f"price success")
            return response
        else:
            print(f"price failed")
            return None


    def rebook_ticket(self,old_order_id, old_trip_id, new_trip_id, new_date, new_seat_type, headers):
        url = f"/api/v1/rebookservice/rebook"

        payload = {
            "oldTripId": old_trip_id,
            "orderId": old_order_id,
            "tripId": new_trip_id,
            "date": new_date,
            "seatType": new_seat_type
        }
        print(payload)
        r = self.client.post(url=url, json=payload, headers=headers)
        if r.status_code == 200:
            print(r.text)
        else:
            print(f"Request Failed: status code: {r.status_code}")
            print(r.text)


    def query_admin_travel(self,headers):
        url = f"/api/v1/admintravelservice/admintravel"

        r = self.client.get(url=url, headers=headers)
        if r.status_code == 200 and r.json()["status"] == 1:
            print("success to query admin travel")
        else:
            print(f"faild to query admin travel with status_code: {r.status_code}")

    def query_one_and_cancel(self,headers, uuid="4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f"):
        """
        查询order并取消order
        :param uuid:
        :param headers:
        :return:
        """
        pairs = self.query_orders(headers=headers, types=tuple([0]))
        pairs2 = self.query_orders(headers=headers, types=tuple([0]), query_other=True)

        if not pairs and not pairs2:
            return

        pairs = pairs + pairs2

        # (orderId, tripId) pair
        pair = self.random_from_list(pairs)
        print(pair[0])
        print("...............................")
        order_id =self.cancel_one_order(order_id=pair[0], uuid=self.uuid, headers=headers)
        if not order_id:
            return

        print(f"{order_id} queried and canceled")

    def query_and_collect_ticket(self,headers):

        pairs = self.query_orders(headers=headers, types=tuple([0]))
        pairs2 = self.query_orders(headers=headers, types=tuple([0]), query_other=True)

        if not pairs and not pairs2:
            return

        pairs = pairs + pairs2

        # (orderId, tripId)
        pair = self.random_from_list(pairs)

        order_id = self.collect_one_order(order_id=pair[0], headers=headers)
        if not order_id:
            return

        print(f"{order_id} queried and collected")

    def query_and_enter_station(self,headers):
        pairs = self.query_orders(headers=headers, types=tuple([0]))
        pairs2 = self.query_orders(headers=headers, types=tuple([0]), query_other=True)

        if not pairs and not pairs2:
            return

        pairs = pairs + pairs2

        # (orderId, tripId)
        pair = self.random_from_list(pairs)

        order_id = self.enter_station(order_id=pair[0], headers=headers)
        if not order_id:
            return

        print(f"{order_id} queried and entered station")

    def query_one_and_put_consign(self,headers, pairs):
        """
        查询order并put consign
        :param uuid:
        :param headers:
        :return:
        """

        pair = self.random_from_list(pairs)

        order_id = self.put_consign(result=pair, headers=headers)
        if not order_id:
            return

        print(f"{order_id} queried and put consign")

    def query_and_rebook(self,headers):

        pairs = self.query_orders(headers=headers, types=tuple([0]))
        print(pairs)
        pairs2 = self.query_orders(headers=headers, types=tuple([1]), query_other=True)

        if not pairs and not pairs2:
            return

        pairs = pairs + pairs2

        # (orderId, tripId)
        pair = self.random_from_list(pairs)
        new_trip_id = "D1345"
        new_date = time.strftime("%Y-%m-%d", time.localtime())
        new_seat_type = "3"

        for pair in pairs: 
            #print(pair)
            self.rebook_ticket(old_order_id=pair[0], old_trip_id=pair[1], new_trip_id=new_trip_id, new_date=new_date, new_seat_type=new_seat_type, headers=headers)

    def query_order_and_pay(self,headers, pairs):
        """
        查询Order并付款未付款Order
        :return:
        """

        # (orderId, tripId) pair
        pair = self.random_from_list(pairs)

        order_id = self.pay_one_order(pair[0], pair[1], headers=headers)
        if not order_id:
            return

        print(f"{order_id} queried and paid")

    def query_travel_left_parallel(self,headers):
        """
        1. 查票（随机高铁或普通）
        2. 查保险、Food、Contacts
        3. 随机选择Contacts、保险、是否买食物、是否托运
        4. 买票
        :return:
        """
        start = ""
        end = ""
        trip_ids = []
        PRESERVE_URL = ""

        start = "Su Zhou"
        end = "Shang Hai"
        high_speed_place_pair = (start, end)
        trip_ids = self.query_high_speed_ticket_parallel(place_pair=high_speed_place_pair, headers=headers, time=time.strftime("%Y-%m-%d", time.localtime()))

    def query_travel_left(self,headers):
        """
        1. 查票（随机高铁或普通）
        2. 查保险、Food、Contacts
        3. 随机选择Contacts、保险、是否买食物、是否托运
        4. 买票
        :return:
        """
        start = ""
        end = ""
        trip_ids = []
        PRESERVE_URL = ""

        high_speed = False
        if high_speed:
            start = "Shang Hai"
            end = "Su Zhou"
            high_speed_place_pair = (start, end)
            trip_ids = self.query_high_speed_ticket(place_pair=high_speed_place_pair, headers=headers, time=time.strftime("%Y-%m-%d", time.localtime()))
        else:
            start = "Shang Hai"
            end = "Nan Jing"
            other_place_pair = (start, end)
            trip_ids = self.query_normal_ticket(place_pair=other_place_pair, headers=headers, time=time.strftime("%Y-%m-%d", time.localtime()))











class WebsiteUser(HttpUser):
    def on_start(self):
        return super().on_start()

    def on_stop(self):
        return super().on_stop()
    host = "http://localhost:30001"
    wait_time = constant(1)
    tasks = [TrainTicketUserTasks]
    #tasks = [BoutiqueUserTasks]
    # tasks = [SockShopUserTasks]
    
class StagesShape(LoadTestShape):
    """
    A simply load test shape class that has different user and spawn_rate at
    different stages.

    Keyword arguments:

        stages -- A list of dicts, each representing a stage with the following keys:
            duration -- When this many seconds pass the test is advanced to the next stage
            users -- Total user count
            spawn_rate -- Number of users to start/stop per second
            stop -- A boolean that can stop that test at a specific stage

        stop_at_end -- Can be set to stop once all stages have run.
    """

    def __init__(self):
        super().__init__()
        lines = []
        with open("/ssj/ssj/train-ticket/train-ticket-auto-query2/sendflow/random-100max.req", 'r') as f:
        #with open("/ssj/ssj/train-ticket/train-ticket-auto-query2/sendflow/normalFlow.req", 'r') as f:
            lines = list(map(int, f.readlines()))
            lines = [x for i,x in enumerate(lines) if i%1==0]#在原来的基础上扩大了4倍
            self.lines = ([1]*5+lines+[1]*5)#又给了几个波谷
            #self.lines = lines#又给了几个波谷
    
    def tick(self):
        run_time = self.get_run_time()
        # for i in range(1, 100):
        #     return (i,1)
        #while True:
        for _ in range(10):#
            for i, v in enumerate(self.lines):
                #if run_time < (i+1)*10:#间隔为10s
                if run_time < (i+1)*5:#间隔为5s
                    tick_data = (v, 100)                
            # user_count -- Total user count
            # spawn_rate -- Number of users to start/stop per second when changing number of users
                    # tick_data = (26, 100)
                    return tick_data
        # for stage in self.stages:
        #     if run_time < stage["duration"]:
        #         tick_data = (stage["users"], stage["spawn_rate"])
        #         return tick_data

 
# if __name__ == '__main__':
#     lines = []
#     with open("/home/meng/random-100max.req", 'r') as f:
#         lines = list(map(int, f.readlines()))
#         lines = [x for i,x in enumerate(lines) if i%3==0]
#     print(len(lines))