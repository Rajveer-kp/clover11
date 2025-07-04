# Google AdSense Configuration for YouTube Management Platform

# Replace these with your actual Google AdSense details
# Get these from your Google AdSense account: https://www.google.com/adsense/

# Your Google AdSense Publisher ID (starts with ca-pub-)
GOOGLE_ADSENSE_PUBLISHER_ID = "ca-pub-1234567890123456"

# Ad Slot IDs for different placements
# Create these in your AdSense account for different ad units
GOOGLE_ADSENSE_SLOTS = {
    "banner": "1234567890",      # 728x90 banner ads
    "sidebar": "0987654321",     # 300x250 sidebar ads  
    "rectangle": "1122334455",   # 300x250 rectangle ads
    "video_page": "5544332211",  # Responsive ads for video pages
    "mobile": "6677889900",      # Mobile-optimized ads
    "inline": "1357924680"       # In-content ads
}

# Ad Settings
GOOGLE_ADSENSE_CONFIG = {
    "enable_auto_ads": True,
    "show_ads_to_logged_in_users": True,
    "show_ads_to_creators": True,
    "show_ads_to_editors": True,
    "ad_frequency": "normal",  # high, normal, low
    "enable_personalized_ads": True
}

# Page-specific ad placements
AD_PLACEMENTS = {
    "dashboard": {
        "banner": True,
        "sidebar": True,
        "auto_ads": True
    },
    "analytics": {
        "banner": True,
        "sidebar": False,
        "auto_ads": True
    },
    "my_videos": {
        "banner": True,
        "sidebar": True,
        "inline": True,
        "auto_ads": True
    },
    "upload": {
        "banner": False,
        "sidebar": True,
        "auto_ads": False  # Don't distract during uploads
    },
    "settings": {
        "banner": True,
        "sidebar": False,
        "auto_ads": True
    }
}

# Revenue sharing (if you want to share revenue with creators)
REVENUE_SHARING = {
    "enabled": False,
    "creator_percentage": 70,  # % of ad revenue for creators
    "platform_percentage": 30  # % of ad revenue for platform
}
