from xml.dom import minidom

content = minidom.parse('ogckml22.xsd')

step = 2
def traverse(node, level):
    nextlevel = level + step
    for child in node.childNodes:
        if child.nodeType != 1:
            continue
        if child.nodeName == "complexType":            
            extensions = child.getElementsByTagName('extension')
            if extensions:
                extension = extensions[0]
                print child.attributes['name'].value, "->", extension.attributes['base'].value.split(':')[-1]
            else:
                print child.attributes['name'].value


        traverse(child, nextlevel)

traverse(content.documentElement, 0)
