import yaml
import xml.etree.ElementTree as xml_tree

with open('feed.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)
    rss_element = xml_tree.Element('rss', {"version":"2.0",
    "xmlns:itunes":"http://www.itunes.com/dtds/podcast-1.0.dtd",
    "xmlns:content":"http://purl.org/rss/1.0/modules/content/"
    })

    channel_element = xml_tree.SubElement(rss_element, 'channel')

    keys = ['title','format', 'subtitle', 'description', 'language', 'link']

    for tags in keys:
        xml_tree.SubElement(channel_element, tags).text = yaml_data[tags]

    
    xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data['author']
    xml_tree.SubElement(channel_element, 'itunes:image', { "href": yaml_data['link']+yaml_data['image']})
    xml_tree.SubElement(channel_element, 'itunes:category', { "text":yaml_data['category']})
    

    item_element = xml_tree.SubElement(channel_element, 'item')
    for items in yaml_data['item']:
        xml_tree.SubElement(channel_element, 'title').text = items['title']
        xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data['author']
        xml_tree.SubElement(channel_element, 'description').text = items['description']
        xml_tree.SubElement(channel_element, 'itunes:duration').text = items['duration']
        xml_tree.SubElement(channel_element, 'pubDate').text = items['published']

        enclosure = xml_tree.SubElement(item_element, 'enclosure', {
            'url':  yaml_data['link']+items['file'],
            'type': 'audio/mpeg',
            'length': items['length']
        })
    
    output_tree = xml_tree.ElementTree(rss_element)
    output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)