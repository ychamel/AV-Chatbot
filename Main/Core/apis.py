import os

import requests

TOPICS = {"events": "return a list of events",
          "cameras": "return a list of camera names",
          "campaigns": "return a list of campaign names",
          "car_counts": "return the number of cars that entered during a certain time",
          "car_parking": "return the plates of the cars currently in the parking",
          "people_count": "return the number of people that entered today or during a certain of given time.",
          # "people_dwelling": "return the number of people that dwelled in front of a certain shop",
          "gates": "return a list of gate names.",
          "shops": "return a list of shop names",
          # "streams": "return a list of camera stream links."
          }


class DataHub:
    def __init__(self):
        self.cache = {}
        self.setup()

    def setup(self):
        # get authentication key
        pass

    def getData(self, Query, Topics):
        """
        data extracter from azkavision api
        :return:
        """
        DATA = {}
        headers = {"Authorization": os.environ.get("AV_TOKEN", None)}
        base_url = "https://arkan.azkavision.com/api/"
        for topic in Topics:
            if topic not in TOPICS.keys():
                # debug topic out of scope
                continue
            # check cache
            if topic in self.cache.keys():
                DATA[topic]=self.cache.get(topic)
                continue

            endpoint = ""
            if topic == "events":
                endpoint = "calendar/events/"
            elif topic == "cameras":
                endpoint = "cameras/"
            elif topic == "campaigns":
                endpoint = "campaigns/"
            elif topic == "car_counts":
                endpoint = "cars/counts-by-gate/"
            elif topic == "car_parking":
                endpoint = "cars/parking/"
            elif topic == "people_count":
                endpoint = "/gates/counter-logs/"
            elif topic == "gates":
                endpoint = "gates/"
            elif topic == "shops":
                endpoint = "shops/"
            # elif topic == "streams":
            #     api_url = "calendar/events/"
            # elif topic == "people_dwelling":
            #     api_url = "calendar/events/"

            response = requests.get(url=base_url + endpoint, headers=headers)
            DATA[topic] = response.json()
            self.cache[topic] = response.json()

        return DATA
