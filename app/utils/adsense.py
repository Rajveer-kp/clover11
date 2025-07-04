"""
Google AdSense integration utilities for YouTube Management Platform
"""

from app.config.adsense_config import (
    GOOGLE_ADSENSE_PUBLISHER_ID, 
    GOOGLE_ADSENSE_SLOTS, 
    GOOGLE_ADSENSE_CONFIG,
    AD_PLACEMENTS
)

def get_adsense_auto_ads_script():
    """Generate the auto ads script for the head section"""
    if not GOOGLE_ADSENSE_CONFIG.get('enable_auto_ads', False):
        return ""
    
    return f'''
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={GOOGLE_ADSENSE_PUBLISHER_ID}"
        crossorigin="anonymous"></script>
    '''

def get_adsense_ad_unit(slot_type="banner", ad_format="auto", style="display:block"):
    """Generate an AdSense ad unit HTML"""
    if slot_type not in GOOGLE_ADSENSE_SLOTS:
        return ""
    
    slot_id = GOOGLE_ADSENSE_SLOTS[slot_type]
    
    return f'''
    <ins class="adsbygoogle"
         style="{style}"
         data-ad-client="{GOOGLE_ADSENSE_PUBLISHER_ID}"
         data-ad-slot="{slot_id}"
         data-ad-format="{ad_format}"
         data-full-width-responsive="true"></ins>
    <script>
         (adsbygoogle = window.adsbygoogle || []).push({{}});
    </script>
    '''

def get_banner_ad():
    """Get a banner ad (728x90)"""
    return get_adsense_ad_unit("banner", "auto", "display:block")

def get_sidebar_ad():
    """Get a sidebar ad (300x250)"""
    return get_adsense_ad_unit("sidebar", "rectangle", "display:block; width:300px; height:250px")

def get_mobile_ad():
    """Get a mobile-optimized ad"""
    return get_adsense_ad_unit("mobile", "auto", "display:block")

def get_inline_ad():
    """Get an inline content ad"""
    return get_adsense_ad_unit("inline", "fluid", "display:block; text-align:center")

def should_show_ads(page, user_role=None):
    """Check if ads should be shown on a specific page for a user role"""
    if not GOOGLE_ADSENSE_CONFIG.get('show_ads_to_logged_in_users', True):
        return False
    
    if user_role == 'creator' and not GOOGLE_ADSENSE_CONFIG.get('show_ads_to_creators', True):
        return False
    
    if user_role == 'editor' and not GOOGLE_ADSENSE_CONFIG.get('show_ads_to_editors', True):
        return False
    
    return page in AD_PLACEMENTS

def get_page_ads(page, user_role=None):
    """Get all ads that should be shown on a specific page"""
    if not should_show_ads(page, user_role):
        return {}
    
    page_config = AD_PLACEMENTS.get(page, {})
    ads = {}
    
    if page_config.get('banner', False):
        ads['banner'] = get_banner_ad()
    
    if page_config.get('sidebar', False):
        ads['sidebar'] = get_sidebar_ad()
    
    if page_config.get('inline', False):
        ads['inline'] = get_inline_ad()
    
    return ads

def get_adsense_revenue_script():
    """Generate revenue tracking script if enabled"""
    if not GOOGLE_ADSENSE_CONFIG.get('enable_personalized_ads', True):
        return ""
    
    return '''
    <script>
        // AdSense revenue tracking
        (adsbygoogle = window.adsbygoogle || []).requestNonPersonalizedAds = 0;
    </script>
    '''

class AdSenseHelper:
    """Helper class for AdSense integration in templates"""
    
    @staticmethod
    def auto_ads_script():
        return get_adsense_auto_ads_script()
    
    @staticmethod
    def banner_ad():
        return get_banner_ad()
    
    @staticmethod
    def sidebar_ad():
        return get_sidebar_ad()
    
    @staticmethod
    def mobile_ad():
        return get_mobile_ad()
    
    @staticmethod
    def inline_ad():
        return get_inline_ad()
    
    @staticmethod
    def page_ads(page, user_role=None):
        return get_page_ads(page, user_role)
    
    @staticmethod
    def should_show(page, user_role=None):
        return should_show_ads(page, user_role)
