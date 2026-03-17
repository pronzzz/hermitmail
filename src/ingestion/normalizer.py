import urllib.parse

def normalize_url(url: str) -> str:
    """
    Normalizes a URL by removing fragment identifiers and common tracking parameters.
    Ensures the URL is complete and canonical.
    """
    if not url:
        return ""
        
    # Ensure scheme
    if not url.lower().startswith(('http://', 'https://')):
        url = 'https://' + url

    parsed = urllib.parse.urlparse(url)
    
    # Strip common tracking parameters
    tracking_params = {
        'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
        'ref', 'source', 'fbclid', 'gclid', '_ga', 'mc_cid', 'mc_eid'
    }
    
    query_params = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    filtered_params = [(k, v) for k, v in query_params if k.lower() not in tracking_params]
    
    # Rebuild query
    new_query = urllib.parse.urlencode(filtered_params)
    
    # Rebuild URL (drop fragment)
    normalized = urllib.parse.urlunparse((
        parsed.scheme.lower(),
        parsed.netloc.lower(),
        parsed.path,
        parsed.params,
        new_query,
        ''  # Strip fragment
    ))
    
    return normalized
