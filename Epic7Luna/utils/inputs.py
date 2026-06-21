import random

# refresh shop confirm
def refresh_confirm(device):
    x_min = 812
    x_max = 1039
    y_min = 539
    y_max = 585
    click_at_area(x_min, x_max, y_min, y_max, device)


# purchase confirm
def purchase_confirm(device):
    x_min = 812
    x_max = 1000
    y_min = 620
    y_max = 660
    click_at_area(x_min, x_max, y_min, y_max, device)


# hit refresh
def click_refresh(device):
    x_min = 100
    x_max = 430
    y_min = 800
    y_max = 850
    click_at_area(x_min, x_max, y_min, y_max, device)


# click within area defined by xmax/xmin and ymax/xmin
def click_at_area(x_min, x_max, y_min, y_max, device):
    x = random.randint(x_min, x_max)
    y = random.randint(y_min, y_max)
    device.shell(f"input tap {x} {y}")
    device.shell(f"input tap {x} {y}")


# scroll down on the shop
def scroll_shop(device):
    device.shell("input swipe 1200 500 1200 300")


# click on purchase
def purchase(device, y):
    x_min = 1455
    x_max = 1550
    x = random.randint(x_min, x_max)
    device.shell(f"input tap {x} {y + 10}")
    device.shell(f"input tap {x} {y + 10}")
