import os
import cPickle
from OpenGL.GL import *
from MtlParser import MtlParser

# this code come partially from the opensource pygame doc 
 
class ObjParser:
    def __init__(self, filename, swapyz=False):
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
            if os.path.isfile(self._cachePath + filename):
                self._loadGlList(filename)
            else:
                raise IOError("File does not exist")
        except Exception, e:
            print("[Warning] Unable to load cache")
            self._parseObjFile(filename, swapyz)
            try:
                self._dumpGlList(filename)
            except Exception, e:
                print("[Warning] Unable to save to cache")
        
    def _dumpGlList(self,filename):
        """ """
        if not os.path.exists(self._cachePath):
            os.makedirs(self._cachePath)
        dumpFile = open(self._cachePath + filename, "wb")
        cPickle.dump(self.__dict__, dumpFile, 2)
        dumpFile.close()

    def _loadGlList(self,filename):
        """ """
        loadFile = open(self._cachePath + filename, "rb")
        tmpDict = cPickle.load(loadFile)
        loadFile.close()
        self.__dict__.update(tmpDict)

    def _parseObjFile(self, filename, swapyz=False):
        """ """
        material = None
        for line in open(self._filePath + filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = map(float, values[1:4])
                if swapyz:
                    v = v[0], v[2], v[1]
                self._vertices.append(v)
            elif values[0] == 'vn':
                v = map(float, values[1:4])
                if swapyz:
                    v = v[0], v[2], v[1]
                self._normals.append(v)
            elif values[0] == 'vt':
                self._textureCoords.append(map(float, values[1:3]))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                self._mtl = MtlParser(self._filePath + values[1])
            elif values[0] == 'f':

                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self._faces.append((face, norms, texcoords, material))

    def build(self, index):
        """ """
        self._mtl.build(index)
        gl_list = glGenLists(index)
        glNewList(gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        for face in self._faces:
            vertices, normals, texture_coords, material = face
            
            texid = self._mtl.texid
            if texid != 0:
                # use diffuse texmap
                glBindTexture(GL_TEXTURE_2D, texid)
            else:
                # just use diffuse colour
                glColor(*mtl['Kd'])
 
            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self._normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2fv(self._textureCoords[texture_coords[i] - 1])
                glVertex3fv(self._vertices[vertices[i] - 1])
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()
        return gl_list
