
class MtlParser:
    def __init__(self, filename):
        self._filePath = "/".join(filename.split("/")[:-1])
        self._filename = filename.split("/")[-1]
        self.mtl = None
        self._parseMtlFile()


    def _parseMtlFile(self):
        for line in open(self._filePath + self._filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'newmtl':
                self.mtl[values[1]] = {}
            elif self.mtl is None:
                raise ValueError, "mtl file doesn't start with newmtl stmt"
            elif values[0] == 'map_Kd':
                # load the texture referred to by this declaration
                self.mtl[values[0]] = values[1]
            else:
                self.mtl[values[0]] = map(float, values[1:])

    def build(self):
        surf = pygame.image.load(self._filePath + self.mtl['map_Kd'])
        image = pygame.image.tostring(surf, 'RGBA', 1)
        ix, iy = surf.get_rect().size
        texid = self.mtl['texture_Kd'] = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,GL_UNSIGNED_BYTE, image)
            