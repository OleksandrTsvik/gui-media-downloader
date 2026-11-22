from models import NavItem
from ui import QIcons
from ui.pages import InstagramPage, VideoPage


NAVIGATION_ITEMS = [
    NavItem(qicon=QIcons.VIDEO, title="Video", page=VideoPage),
    NavItem(qicon=QIcons.MUSIC, title="Music", page=VideoPage),
    NavItem(qicon=QIcons.YOUTUBE, title="YouTube", page=VideoPage),
    NavItem(qicon=QIcons.INSTAGRAM, title="Instagram", page=InstagramPage),
    NavItem(qicon=QIcons.TIKTOK, title="TikTok", page=InstagramPage),
]
