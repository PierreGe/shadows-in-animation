import os
from MtlParser import MtlParser

from vispy.io import imread, read_mesh, load_data_file

# this code come partially from the opensource pygame doc 
 
class ObjParser:
    def __init__(self, filename):
        """Loads a Wavefront OBJ file. """

        self._filePath = "/".join(filename.split("/")[:-1])
        filename = filename.split("/")[-1]
        if len(self._filePath) >0 and self._filePath[-1] != "/":
            self._filePath += "/"
        self._cachePath = self._filePath.replace("assets/", "cache/", 1)

        self._vertices = []
        self._normals = []
        self._textureCoords = []
        self._faces = []
        self._mtl = None
        try:
            if os.path.isfile(self._filePath + filename):
                self._parseObjFile(filename)
            else:
                raise IOError("File does not exist")
        except Exception, e:
            print("[ERROR] Unable to load object")

    def getVertices(self):
        return self._vertices

    def getNormals(self):
        return self._normals

    def getTextureCoords(self):
        return self._textureCoords

    def getFaces(self):
        return self._faces

    def getMtl(self):
        return self._mtl

    def _parseObjFile(self, filename):
        """ """
        self._vertices, self._faces, self._normals, self._textureCoords = read_mesh(self._filePath + filename)
        

        # material = None
        # for line in open(self._filePath + filename, "r"):
        #     if line.startswith('#'): continue
        #     values = line.split()
        #     if not values: continue
        #     if values[0] == 'v':
        #         v = map(float, values[1:4])
        #         if swapyz:
        #             v = v[0], v[2], v[1]
        #         self._vertices.append(v)
        #     elif values[0] == 'vn':
        #         v = map(float, values[1:4])
        #         if swapyz:
        #             v = v[0], v[2], v[1]
        #         self._normals.append(v)
        #     elif values[0] == 'vt':
        #         self._textureCoords.append(map(float, values[1:3]))
        #     elif values[0] in ('usemtl', 'usemat'):
        #         material = values[1]
        #     elif values[0] == 'mtllib':
        #         self._mtl = MtlParser(self._filePath + values[1])
        #     elif values[0] == 'f':

        #         face = []
        #         texcoords = []
        #         norms = []
        #         for v in values[1:]:
        #             w = v.split('/')
        #             face.append(int(w[0]))
        #             if len(w) >= 2 and len(w[1]) > 0:
        #                 texcoords.append(int(w[1]))
        #             else:
        #                 texcoords.append(0)
        #             if len(w) >= 3 and len(w[2]) > 0:
        #                 norms.append(int(w[2]))
        #             else:
        #                 norms.append(0)
        #         self._faces.append((face, norms, texcoords, material))

