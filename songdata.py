from xml.etree import ElementTree

class SongData:
    def __init__(self, file_path):
        self.file_path = file_path
        
        dt = ElementTree.parse(self.file_path)
        self.lyrics = getattr(dt.find('lyrics'), 'text', '') or ''
        self.title = getattr(dt.find('title'), 'text', '') or ''
        self.author = getattr(dt.find('author'), 'text', '') or ''
        self.copyright = getattr(dt.find('copyright'), 'text', '') or ''
        self.ccli = getattr(dt.find('ccli'), 'text', '') or ''

        self.capo = ''
        self.capo_print = False
        capo_data = dt.find('capo')

        if (capo_data is not None):
            self.capo = capo_data.text
            self.capo_print = capo_data.attrib.get('print', '') == 'true'

        self.key = getattr(dt.find('key'), 'text', '') or ''

    def set_element(self, tree, root, name, value):
        t = tree.find(name)
        if (t is not None):
            t.text = value
        else:
            e = ElementTree.Element(name)
            e.text = value
            root.append(e)

    def save(self):
        dt = ElementTree.parse(self.file_path)
        r = dt.getroot()

        self.set_element(dt, r, 'lyrics', self.lyrics)
        self.set_element(dt, r, 'title', self.title)
        self.set_element(dt, r, 'author', self.author)
        self.set_element(dt, r, 'copyright', self.copyright)
        self.set_element(dt, r, 'ccli', self.ccli)

        cp = dt.find('capo')
        if (cp is not None):
            cp.text = self.capo
            cp.set('print', str(self.capo_print).lower())
        else:
            e = ElementTree.Element('capo')
            e.text = self.capo
            e.set('print', str(self.capo_print).lower())
            r.append(e)

        dt.write(self.file_path)