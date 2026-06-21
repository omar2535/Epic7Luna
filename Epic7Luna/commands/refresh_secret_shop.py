from ppadb.device import Device
from utils.resource_manager import get_gold_and_gems
from utils.inputs import scroll_shop, refresh_confirm, purchase_confirm, click_refresh, purchase
from Epic7Luna.config import config
from Epic7Luna.utils.image_utils import find_covenant_bookmarks, find_mystic_bookmarks, find_friendship_bookmarks, take_screenshot


import time


class RefreshSecretShop:
    num_covenant_purchases = 0
    num_mystic_purchases = 0
    num_refreshes = 0

    def __init__(self, device: Device):
        self.device = device

    def refresh(self, device: Device):
        mystics_seen = 0
        covenants_seen = 0

        print(f"---Starting shop refresher. MIN_GEMS: {config.GEMS_MIN}, MIN_GOLD: {config.GOLD_MIN} ---")

        while True:
            # check top of shop
            self.check_for_bookmarks_and_purchase(device, covenants_seen, mystics_seen)

            # scroll down to bottom of shop
            time.sleep(0.3)
            scroll_shop(device)
            time.sleep(0.3)

            # check bottom of shop
            self.check_for_bookmarks_and_purchase(device, covenants_seen, mystics_seen)

            # sleep for a bit before refreshing
            time.sleep(0.3)

            # refresh
            click_refresh(device)
            time.sleep(0.3)
            refresh_confirm(device)
            time.sleep(0.5)
            self.num_refreshes += 1

            # update stats
            self.update_stats_file()

            # if resource count not above threshold, stop the program
            if not self.is_resource_count_above_threshold():
                break

        print("---Program complete---")

    def check_for_bookmarks_and_purchase(self, device, covenants_seen: int, mystics_seen: int):
        time.sleep(1)
        take_screenshot(device)
        covenant_bookmarks_location = find_covenant_bookmarks()
        mystic_bookmarks_location = find_mystic_bookmarks()
        friendship_bookmarks_location = find_friendship_bookmarks()
        if covenant_bookmarks_location != (0, 0):
            purchase(device, covenant_bookmarks_location[1])
            time.sleep(0.1)
            purchase_confirm(device)
            self.num_covenant_purchases += 1
        if mystic_bookmarks_location != (0, 0):
            purchase(device, mystic_bookmarks_location[1])
            time.sleep(0.1)
            purchase_confirm(device)
            self.num_mystic_purchases += 1
        if friendship_bookmarks_location != (0, 0):
            purchase(device, friendship_bookmarks_location[1])
            time.sleep(0.1)
            purchase_confirm(device)

    def is_resource_count_above_threshold(self):
        try:
            gold, gems = get_gold_and_gems()
            print(f"Current gold: {int(gold)}, current gems: {int(gems)}")
            if (int(gold) <= config.GOLD_MIN or int(gems) <= config.GEMS_MIN):
                return False
        except Exception as e:
            print(f"Couldn't do OCR: {e}")
            return True
        return True

    def update_stats_file(self):
        """Updates the stats file with the current number of purchases and refreshes.
        """
        f = open("stats.txt", "w")
        f.write(f"Num covenant bookmarks: {self.num_covenant_purchases}, Covenant bookmarks purchased: {self.num_covenant_purchases * 5}\n")
        f.write(f"Num mystic bookmarks: {self.num_mystic_purchases}, Mystic bookmarks purchased: {self.num_mystic_purchases * 50}\n")
        f.write(f"Num refreshes: {self.num_refreshes}, Skystones spent: {self.num_refreshes * 3}\n")
        f.write(f"Covernant rate: {round(float(self.num_covenant_purchases) / float(self.num_refreshes) * 100, 2)}%\n")
        f.write(f"Mystic rate: {round(float(self.num_mystic_purchases) / float(self.num_refreshes) * 100, 2)}%\n")
        f.close()
