from ppadb.device import Device
from Epic7Luna.config import config
from Epic7Luna.utils.resource_manager import get_gold_and_gems
from Epic7Luna.utils.inputs import scroll_shop, refresh_confirm, purchase_confirm, click_refresh, purchase
from Epic7Luna.utils.image_utils import find_covenant_bookmarks, find_mystic_bookmarks, find_friendship_bookmarks, take_screenshot


import time


class RefreshSecretShop:
    def __init__(self, device: Device):
        self.device = device
        self.num_covenant_purchases = 0
        self.num_mystic_purchases = 0
        self.num_friendship_purchases = 0
        self.num_refreshes = 0

    def refresh(self, device: Device):
        print(f"---Starting shop refresher. MIN_GEMS: {config.GEMS_MIN}, MIN_GOLD: {config.GOLD_MIN} ---")

        while True:
            # check top of shop
            self.check_for_bookmarks_and_purchase(device)

            # scroll down to bottom of shop
            time.sleep(0.3)
            scroll_shop(device)
            time.sleep(0.3)

            # check bottom of shop
            self.check_for_bookmarks_and_purchase(device)

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

    def check_for_bookmarks_and_purchase(self, device):
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
            self.num_friendship_purchases += 1

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
        stats = "\n".join(self.get_stats_lines()) + "\n"

        with open("stats.txt", "w") as f:
            f.write(stats)

        print(self.get_stats_line())

    def get_stats_lines(self):
        """Builds the stats summary for file output."""
        covenant_rate = self.get_purchase_rate(self.num_covenant_purchases)
        mystic_rate = self.get_purchase_rate(self.num_mystic_purchases)
        friendship_rate = self.get_purchase_rate(self.num_friendship_purchases)

        return [
            f"Num covenant purchases: {self.num_covenant_purchases}, Covenant bookmarks purchased: {self.num_covenant_purchases * 5}",
            f"Num mystic purchases: {self.num_mystic_purchases}, Mystic bookmarks purchased: {self.num_mystic_purchases * 50}",
            f"Num friendship purchases: {self.num_friendship_purchases}",
            f"Num refreshes: {self.num_refreshes}, Skystones spent: {self.num_refreshes * 3}",
            f"Covenant rate: {covenant_rate}%",
            f"Mystic rate: {mystic_rate}%",
            f"Friendship rate: {friendship_rate}%",
        ]

    def get_stats_line(self):
        """Builds the stats summary for console printing."""
        return " | ".join(self.get_stats_lines())

    def get_purchase_rate(self, num_purchases: int) -> float:
        if self.num_refreshes == 0:
            return 0.0

        return round(float(num_purchases) / float(self.num_refreshes) * 100, 2)
