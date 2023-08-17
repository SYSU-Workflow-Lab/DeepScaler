from locust import HttpUser, TaskSet, task, constant
from locust import LoadTestShape
import random
from random import randint, choice
import base64

class BookInfoUserTasks(TaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        

    @task(1)
    def get_productpage(self):
        self.client.get("/productpage")
    
    @task(1)
    def get_details(self):
        self.client.get("/details")

    @task(1)
    def get_reviews(self):
        self.client.get("/reviews")
    
    @task(1)
    def get_ratings(self):
        self.client.get("/ratings")

class BoutiqueUserTasks(TaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.products = [
            '0PUK6V6EV0',
            '1YMWWN1N4O',
            '2ZYFJ3GM2N',
            '66VCHSJNUP',
            '6E92ZMYYFZ',
            '9SIQT8TOJO',
            'L9ECAV7KIM',
            'LS4PSXUNUM',
            'OLJCESPC7Z']
    #
    @task(1)
    def index(self):
        self.client.get("/")
    #
    @task(2)
    def setCurrency(self):
        currencies = ['EUR', 'USD', 'JPY', 'CAD']
        self.client.post("/setCurrency",
            {'currency_code': random.choice(currencies)})
    @task(10)
    def browseProduct(self):
        self.client.get("/product/" + random.choice(self.products))

    @task(2)
    def viewCart(self):
        self.client.get("/cart")

    @task(3)
    def addToCart(self):
        product = random.choice(self.products)
        self.client.get("/product/" + product)
        self.client.post("/cart", {
            'product_id': product,
            'quantity': random.choice([1,2,3,4,5,10])})

    @task(1)
    def checkout(self):
        self.addToCart()
        self.client.post("/cart/checkout", {
            'email': 'someone@example.com',
            'street_address': '1600 Amphitheatre Parkway',
            'zip_code': '94043',
            'city': 'Mountain View',
            'state': 'CA',
            'country': 'United States',
            'credit_card_number': '4432-8015-6152-0454',
            'credit_card_expiration_month': '1',
            'credit_card_expiration_year': '2039',
            'credit_card_cvv': '672',
        })

class SockShopUserTasks(TaskSet):
    def __init__(self, parent):
        super().__init__(parent)
    
    @task(1)
    def index(self):
        self.client.get("/")
        
    @task(1)
    def catalogue(self):
        # catalogue = self.client.get("/catalogue").json()
        # category_item = choice(catalogue)
        # item_id = category_item["id"]
        self.client.get("/catalogue")
        self.client.get("/category.html")

    @task(1)
    def login(self):
        base64string = base64.encodestring(('%s:%s' % ('user', 'password')).encode()).decode().replace('\n', '')
        self.client.get("/login", headers={"Authorization":"Basic %s" % base64string})

    @task(1)
    def detail(self):
        self.client.get("/detail.html?id=3395a43e-2d88-40de-b95f-e00e1502085b")

    @task(1)
    def cart(self):
        self.client.delete("/cart")
        self.client.post("/cart", json={"id": '3395a43e-2d88-40de-b95f-e00e1502085b', "quantity": 1})

    @task(1)
    def basket(self):
        self.client.get("/basket.html")
    
    @task(1)
    def orders(self):
        self.client.post("/orders")

class WebsiteUser(HttpUser):
    def on_start(self):
        return super().on_start()

    def on_stop(self):
        return super().on_stop()
    host = "http://localhost:30001"
    wait_time = constant(1)
    # tasks = [BookInfoUserTasks]
    tasks = [BoutiqueUserTasks]
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
        with open("/sendflow/random-100max.req", 'r') as f:
        #with open("/home/ssj/boutiquessj/pyboutique/sendflow/normalFlow.req", 'r') as f:
            lines = list(map(int, f.readlines()))
            lines = [x for i,x in enumerate(lines) if i%1==0]
            self.lines = ([1]*5+lines+[1]*5)
            #self.lines = lines
    
    def tick(self):
        run_time = self.get_run_time()
        # for i in range(1, 100):
        #     return (i,1)
        #while True:
        for _ in range(10):#
            for i, v in enumerate(self.lines):
                #if run_time < (i+1)*10:#internal 10s
                if run_time < (i+1)*5:#internal为5
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
