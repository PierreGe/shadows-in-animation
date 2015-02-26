#include <cstdio>
#include <cstdlib>
#include <set>
#include <vector>
#include <iostream>

class Vector {
public:
	float x;
	float y;
	float z;
	bool operator==(const Vector& other) {
		return this->x == other.x and this->y == other.y and this->z == other.z;
	}
	Vector(){}
	Vector(float floats[3]){
		this->x = floats[0];
		this->y = floats[1];
		this->z = floats[2];
	}
	operator float*() {
		float* ret = new float[3];
		ret[0] = this->x;
		ret[1] = this->y;
		ret[2] = this->z;
		return ret;
	}
};

class Edge {
public:
	Vector one;
	Vector two;
	bool operator==(const Edge& other) {
		return this->one == other.one and this->two == other.two;
	}
	operator Vector*() {
		Vector* ret = new Vector[2];
		ret[0] = this->one;
		ret[1] = this->two;
		return ret;
	}
};

std::ostream& operator<<(std::ostream& out, const Vector& vec) {
	out << "[" << vec.x << "," << vec.y << "," << vec.z << "]";
	return out;
}

std::ostream& operator<<(std::ostream& out, const Edge& edge) {
	out << "[" << edge.one << "," << edge.two << "]";
	return out;
}

class Triangle {
public:
	Vector one;
	Vector two;
	Vector three;
	bool operator==(const Triangle& other) {
		return this->one == other.one and this->two == other.two and this->three == other.three;
	}
};

void subtract(Vector* vector1, Vector* vector2, Vector* res) {
	res->x = vector1->x - vector2->x;
	res->y = vector1->y - vector2->y;
	res->z = vector1->z - vector2->z;
}

void cross(Vector* vector1, Vector* vector2, Vector* res) {
	res->x = vector1->y * vector2->z - vector1->z * vector2->y;
	res->y = vector1->z * vector2->x - vector1->x * vector2->z;
	res->z = vector1->x * vector2->y - vector1->y * vector2->x;
}

float dot(Vector* vector1, Vector* vector2) {
	return vector1->x * vector2->x + vector1->y * vector2->y + vector1->z * vector2->z;
}

void computeAverageTrianglePosition(Triangle* triangle, Vector* ret) {
	int sumX = 0, sumY = 0, sumZ = 0;
	int i;
	Vector* triangleXYZ = (Vector*) triangle;
	for (i = 0; i < 3; ++i) {
		sumX += triangleXYZ[i].x;
		sumY += triangleXYZ[i].y;
		sumZ += triangleXYZ[i].z;
	}
	ret->x = sumX/3;
	ret->y = sumY/3;
	ret->z = sumZ/3;
}

bool erase(std::vector<Edge>& edges, Edge& edge1, Edge& edge2) {
	int size_vec = edges.size();
	for (int i = 0; i < size_vec; ++i) {
		if (edges[i] == edge1 or edges[i] == edge2) {
			edges.erase(edges.begin()+i);
			return true;
		}
	}
	return false;
}

Edge* findContourEdges2(Vector* positions, int* indices, Vector* normals, 
					   int sizeIndices, Vector lightPosition) {
	// for (int i = 0; i < 8; ++i) {
	// 	std::cout << positions[i][0] << "," << positions[i][1] << "," << positions[i][2] << std::endl;
	// }
	// for (int i = 0; i < sizeIndices; ++i) {
	// 	std::cout << indices[i]  << std::endl;
	// }
	// for (int i = 0; i < 8; ++i) {
	// 	std::cout << normals[i][0] << "," << normals[i][1] << "," << normals[i][2] << std::endl;
	// }

	int index_indices;
	Triangle triangle;
	Vector averageTrianglePos;
	Vector lightDir;
	Vector triangleDir1, triangleDir2;
	Vector triangleNormal;
	std::vector<Edge> returnVec;
	for (index_indices = 0; index_indices < sizeIndices; ++index_indices) {
		int a = indices[index_indices], b = indices[index_indices+1], c = indices[index_indices+2];
		triangle.one = positions[a];
		triangle.two = positions[b];
		triangle.three = positions[c];
		computeAverageTrianglePosition(&triangle, &averageTrianglePos);
		subtract(&averageTrianglePos, &lightPosition, &lightDir);
		subtract(&triangle.two, &triangle.one, &triangleDir1);
		subtract(&triangle.three, &triangle.one, &triangleDir2);
		cross(&triangleDir1, &triangleDir2, &triangleNormal);
		if (dot(&lightDir, &triangleNormal) >= 0) {
			Edge edges[3];
			edges[0].one = triangle.one;
			edges[0].two = triangle.two;
			edges[1].one = triangle.one;
			edges[1].two = triangle.three;
			edges[2].one = triangle.two;
			edges[2].two = triangle.three;
			Edge reverseEdges[3];
			reverseEdges[0].two = triangle.one;
			reverseEdges[0].one = triangle.two;
			reverseEdges[1].two = triangle.one;
			reverseEdges[1].one = triangle.three;
			reverseEdges[2].two = triangle.two;
			reverseEdges[2].one = triangle.three;
			for (int i = 0; i < 3; ++i){ // for each edge
				if (not erase(returnVec, edges[i], reverseEdges[i])) {
					returnVec.push_back(edges[i]);
				}
			}
		}
	}
	Edge* returnEdges = new Edge[returnVec.size()];
	std::vector<Edge>::iterator it;
	int i = 0;
	for (it = returnVec.begin(); it != returnVec.end(); ++it) {
		returnEdges[i++] = *it;
		std::cout << (*it) << std::endl;
	}
	return returnEdges;
}
	        // positions = self._objects[index].getVertices()
	        // indices = self._objects[index].getIndices()
	        // normals = self._objects[index].getNormals()
	        // ret = trianglenumpy.array([])
	        // lightPosition = numpy.dot(self._light.getPosition() + [0], numpy.linalg.inv(self._model))
	        // for i in range(0,len(indices), 3):
	        //     a = indices[i]
	        //     b = indices[i+1]
	        //     c = indices[i+2]
	        //     triangle = numpy.array([positions[a], positions[b], positions[c]])
	        //     averageTrianglePos = numpy.array([sum([x[0] for x in triangle])/3.0,
	        //                           sum([x[1] for x in triangle])/3.0,
	        //                           sum([x[2] for x in triangle])/3.0, 0.0])
        	//     lightDir = numpy.subtract(averageTrianglePos, lightPosition)
        	//     triangleNormal = numpy.append(numpy.cross(numpy.subtract(triangle[1], triangle[0]), numpy.subtract(triangle[2], triangle[0])), numpy.array([1]))
        	//     if numpy.dot(lightDir, triangleNormal) >= 0:
        	//         for edge in numpy.nditer(numpy.array([[positions[a], positions[b]],[positions[a], positions[c]],[positions[b], positions[c]]])):
        	//             if edge in ret.tolist() or [edge[1], edge[0]] in ret.tolist():
        	//                 try:
        	//                     ret.remove(edge)
        	//                 except Exception, e:
        	//                     ret.remove([edge[1], edge[0]])
        	//             else:
        	//                 numpy.append(ret,edge)
        	// return ret


extern "C" {
	Edge* findContourEdges(Vector* positions, int* indices, Vector* normals,
					       int sizeIndices, Vector lightPosition)
	{
		return findContourEdges2(positions, indices, normals, sizeIndices, lightPosition);
	}
}

int main(int argc, char** argv) {
	return 0;
}

