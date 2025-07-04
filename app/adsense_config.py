# Google AdSense Configuration
# Update these values with your actual AdSense details

ADSENSE_CONFIG = {
    'publisher_id': 'ca-pub-5425864168922727',
    'auto_ads_enabled': True,
    'ad_slots': {
        'main_banner': '1283888354',
        'sidebar_rectangle': '1283888354', 
        'video_page': '1283888354',
        'footer_banner': '1283888354',
        'mobile_banner': '1283888354'
    },
    'ad_formats': {
        'banner': 'leaderboard',
        'sidebar': 'rectangle', 
        'mobile': 'auto',
        'responsive': 'auto'
    }
}

def get_adsense_script_tag():
    """Returns the main AdSense script tag"""
    return f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CONFIG["publisher_id"]}" crossorigin="anonymous"></script>'

def get_ad_unit(slot_name='main_banner', ad_format='auto', responsive=True):
    """
    Generate AdSense ad unit HTML
    
    Args:
        slot_name: Key from ad_slots config
        ad_format: Ad format (auto, rectangle, leaderboard, etc.)
        responsive: Whether to make the ad responsive
    """
    slot_id = ADSENSE_CONFIG['ad_slots'].get(slot_name, ADSENSE_CONFIG['ad_slots']['main_banner'])
    
    responsive_attr = 'data-full-width-responsive="true"' if responsive else ''
    
    return f'''
    <ins class="adsbygoogle"
         style="display:block"
         data-ad-client="{ADSENSE_CONFIG['publisher_id']}"
         data-ad-slot="{slot_id}"
         data-ad-format="{ad_format}"
         {responsive_attr}></ins>
    <script>
         (adsbygoogle = window.adsbygoogle || []).push({{}});
    </script>
    '''

def get_auto_ads_script():
    """Returns the auto ads initialization script"""
    if not ADSENSE_CONFIG['auto_ads_enabled']:
        return ''
    
    return f'''
    <script>
        window.addEventListener('load', function() {{
            (adsbygoogle = window.adsbygoogle || []).push({{
                google_ad_client: "{ADSENSE_CONFIG['publisher_id']}",
                enable_page_level_ads: true
            }});
        }});
    </script>
    '''
