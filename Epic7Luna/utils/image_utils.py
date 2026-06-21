import cv2
import pyautogui
import numpy as np


def find_subimage_center(im1, im2):
    haystack = cv2.imread(im1)
    needle = cv2.imread(im2)

    height, width, channels = needle.shape

    result = cv2.matchTemplate(needle, haystack, cv2.TM_CCOEFF_NORMED)
    y, x = np.unravel_index(result.argmax(), result.shape)

    return x + (width / 2), y + (height / 2)


# finds the 3/4 point y point of an image
# which is half below the center line
def find_subimage_low_x(im1, im2):
    haystack = cv2.imread(im1)
    needle = cv2.imread(im2)

    height, width, channels = needle.shape

    result = cv2.matchTemplate(needle, haystack, cv2.TM_CCOEFF_NORMED)
    y, x = np.unravel_index(result.argmax(), result.shape)

    return y + (height * 3 / 4)


# returns x and y cordinates
# of covenant bookmark location on the screen
def find_covenant_bookmarks() -> tuple:
    try:
        result = pyautogui.locate(
            "matches/covenant_bookmarks.png", "screenshots/screen.png", confidence=0.8
        )
        if result is None:
            return 0, 0
    except pyautogui.ImageNotFoundException:
        return 0, 0
    return result.left + result.width / 2, result.top + result.height * 3 / 4


# returns x and y cordinates
# of mystic bookmarks location on the screen
def find_mystic_bookmarks() -> tuple:
    try:
        result = pyautogui.locate(
            "matches/mystic_bookmarks.png", "screenshots/screen.png", confidence=0.8
        )
        if result is None:
            return 0, 0
    except pyautogui.ImageNotFoundException:
        return 0, 0
    return result.left + result.width / 2, result.top + result.height * 3 / 4

# returns x and y cordinates
# of friendship bookmarks location on the screen
def find_friendship_bookmarks() -> tuple:
    try:
        result = pyautogui.locate(
            "matches/friendship_bookmarks.png", "screenshots/screen.png", confidence=0.8
        )
        if result is None:
            return 0, 0
    except pyautogui.ImageNotFoundException:
        return 0, 0
    return result.left + result.width / 2, result.top + result.height * 3 / 4

def find_purchase_covenant() -> tuple:
    """Finds the purchase covenant button on the screen.
    Returns the x and y coordinates of the button.

    Returns:
        tuple (x, y): The x and y coordinates of the button.
    """
    try:
        result = pyautogui.locate(
            "matches/purchase_covenant.png", "screenshots/screen.png", confidence=0.8
        )
        if result is None:
            return 0, 0
    except pyautogui.ImageNotFoundException:
        return 0, 0
    return result.left + result.width / 2, result.top + result.height * 3 / 4


def find_buy_confirm() -> tuple:
    """Finds the buy confirm button on the screen.
    Returns the x and y coordinates of the button.

    Returns:
        tuple (x, y): The x and y coordinates of the button.
    """
    try:
        result = pyautogui.locate(
            "matches/buy_confirm.png", "screenshots/screen.png", confidence=0.8
        )
        if result is None:
            return 0, 0
    except pyautogui.ImageNotFoundException:
        return 0, 0
    return result.left + result.width / 2, result.top + result.height * 3 / 4


# takes a screenshot
# saves in screenshots/screen.png
def take_screenshot(device):
    result = device.screencap()
    with open("screenshots/screen.png", "wb") as fp:
        fp.write(result)
