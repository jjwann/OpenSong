from xml.etree import ElementTree

class SongData:
    """Contains the relevant song data
    """
    def __init__(self, file_path):
        """
            Args:
                file_path: The path of the file from which to retrieve song information
        """
        self.file_path = file_path
        pe = ElementTree.ParseError("File is not in proper OpenSong format")

        #The file should be in XML format and the root tag should be "song"
        try:
            dt = ElementTree.parse(self.file_path)
        except ParseError:
            raise pe

        r = dt.getroot()
        if r.tag.lower() != 'song':
            raise pe

        #Extract the song data from the file
        self.lyrics = getattr(dt.find('lyrics'), 'text', '') or ''
        self.title = getattr(dt.find('title'), 'text', '') or ''
        self.author = getattr(dt.find('author'), 'text', '') or ''
        self.copyright = getattr(dt.find('copyright'), 'text', '') or ''
        self.ccli = getattr(dt.find('ccli'), 'text', '') or ''
        self.presentation = getattr(dt.find('presentation'), 'text', '') or ''

        self.capo = ''
        self.capo_print = False
        capo_data = dt.find('capo')

        if capo_data is not None:
            self.capo = capo_data.text
            self.capo_print = capo_data.attrib.get('print', '') == 'true'

        self.key = getattr(dt.find('key'), 'text', '') or ''

    def save(self):
        #Saves the song data back to the file
        def set_element(root, name, value):
            """Sets the value of the element or creates a new element

                Args:
                    root: The root element where the element can be found/appended to
                    name: The name of the element tag
                    value: The value of the element
            """
            t = root.find(name)
            if t is not None:
                t.text = value
            else:
                e = ElementTree.Element(name)
                e.text = value
                root.append(e)
        
        dt = ElementTree.parse(self.file_path)
        r = dt.getroot()

        set_element(r, 'lyrics', self.lyrics)
        set_element(r, 'title', self.title)
        set_element(r, 'author', self.author)
        set_element(r, 'copyright', self.copyright)
        set_element(r, 'ccli', self.ccli)
        set_element(r, 'presentation', self.presentation)
        set_element(r, 'key', self.key)

        #Create a new capo element if one is not found
        cp = dt.find('capo')
        if cp is not None:
            cp.text = self.capo
            cp.set('print', str(self.capo_print).lower())
        else:
            e = ElementTree.Element('capo')
            e.text = self.capo
            e.set('print', str(self.capo_print).lower())
            r.append(e)

        dt.write(self.file_path)
