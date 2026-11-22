from config import QIcons
from models import NavItem
from ui.widgets import InstagramPage, YouTubePage


NAVIGATION_ITEMS = [
    NavItem(qicon=QIcons.YOUTUBE, title="YouTube", page=YouTubePage),
    NavItem(qicon=QIcons.INSTAGRAM, title="Instagram", page=InstagramPage),
    NavItem(qicon=QIcons.INSTAGRAM, title="History", page=InstagramPage),
    NavItem(qicon=QIcons.INSTAGRAM, title="Settings", page=InstagramPage),
]
