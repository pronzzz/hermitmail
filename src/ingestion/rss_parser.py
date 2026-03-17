import xml.etree.ElementTree as ET
from typing import List

def parse_rss_links(xml_content: str) -> List[str]:
    """
    Parses an RSS or Atom feed XML string and extracts all article links.
    Returns a list of URLs.
    """
    links = []
    try:
        root = ET.fromstring(xml_content)
        
        # Determine if it's RSS or Atom
        if root.tag == 'rss' or root.tag.endswith('rss'):
            # It's an RSS feed: look for channel/item/link
            for item in root.findall('.//item'):
                link_elem = item.find('link')
                if link_elem is not None and link_elem.text:
                    links.append(link_elem.text.strip())
        elif 'feed' in root.tag or root.tag.endswith('feed'):
            # It's an Atom feed: look for entry/link
            # Atom feeds often use namespaces, e.g., {http://www.w3.org/2005/Atom}entry
            # For simplicity, we can strip the namespace or use a general search
            for entry in root.findall('.//*'):
                if entry.tag.endswith('entry'):
                    for link_elem in entry.findall('.//*'):
                        if link_elem.tag.endswith('link'):
                            # Atom links are usually in an 'href' attribute
                            if 'href' in link_elem.attrib:
                                # We only want alternate links, not self-referential feed links
                                rel = link_elem.attrib.get('rel', 'alternate')
                                if rel == 'alternate':
                                    links.append(link_elem.attrib['href'].strip())
    except ET.ParseError:
        pass # Malformed XML
        
    return links
