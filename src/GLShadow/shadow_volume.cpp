#include <cstdio>
#include <cstdlib>
#include <set>
#include <vector>
#include <iostream>
#include <ctime>
#include <unordered_set>

class Vector {
public:
	float x;
	float y;
	float z;
	bool operator==(const Vector& other) const {
		return this->x == other.x and this->y == other.y and this->z == other.z;
	}
	Vector(){}
	Vector(float floats[3]){
		this->x = floats[0];
		this->y = floats[1];
		this->z = floats[2];
	}
};

namespace std
{
	template<>
	struct hash<Vector> {
	    size_t operator()(const Vector &vec) const {
	        return std::hash<float>()(vec.x) ^ std::hash<float>()(vec.y) ^ std::hash<float>()(vec.z);
	    }
	};
}

class Edge {
public:
	Vector one;
	Vector two;
	bool operator==(const Edge& other) const {
		return this->one == other.one and this->two == other.two;
	}
};

namespace std
{
	template<>
	struct hash<Edge> {
		size_t operator()(const Edge &edge) const {
			return std::hash<Vector>()(edge.one) ^ std::hash<Vector>()(edge.two);
		}
	};
}

class Triangle {
public:
	Vector one;
	Vector two;
	Vector three;
	bool operator==(const Triangle& other) const {
		return this->one == other.one and this->two == other.two and this->three == other.three;
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

std::ostream& operator<<(std::ostream& out, const Triangle& triangle) {
	out << "[" << triangle.one << "," << triangle.two << "," << triangle.three << "]";
	return out;
}

void add(Vector* vector1, Vector* vector2, Vector* res) {
	res->x = vector1->x + vector2->x;
	res->y = vector1->y + vector2->y;
	res->z = vector1->z + vector2->z;
}

void subtract(Vector* vector1, Vector* vector2, Vector* res) {
	res->x = vector1->x - vector2->x;
	res->y = vector1->y - vector2->y;
	res->z = vector1->z - vector2->z;
}

void divide(Vector* vector, float divi) {
	vector->x /= divi;
	vector->y /= divi;
	vector->z /= divi;
}

void cross(Vector* vector1, Vector* vector2, Vector* res) {
	res->x = vector1->y * vector2->z - vector1->z * vector2->y;
	res->y = vector1->z * vector2->x - vector1->x * vector2->z;
	res->z = vector1->x * vector2->y - vector1->y * vector2->x;
}

float dot(Vector* vector1, Vector* vector2) {
	return vector1->x * vector2->x + vector1->y * vector2->y + vector1->z * vector2->z;
}


bool counterclockwise(Vector* vector1, Vector* vector2, Vector* center, Vector* normal) {
	Vector first, second, crossProd;
	subtract(vector1, center, &first);
	subtract(vector2, center, &second);
	cross(&first, &second, &crossProd);
	return dot(normal, &crossProd) >= 0;
}


void computeTriangleCenter(Triangle* triangle, Vector* ret) {
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

void findContourEdges2(Vector* positions, int* indices, Vector* normals, 
					   int sizeIndices, Vector lightPosition, Edge* returnEdges, int* returnSize) {
	std::unordered_set<Edge> edgesSet;
	int index_indices;
	Triangle triangle;
	Vector triangleCenter;
	Vector lightDir;
	Vector triangleDir1, triangleDir2;
	Vector triangleNormal;
	float total_iter = 0, total_erase = 0;
	for (index_indices = 0; index_indices < sizeIndices; index_indices+=3) {
		clock_t time_beg = clock();
		int a = indices[index_indices], b = indices[index_indices+1], c = indices[index_indices+2];
		triangle.one = positions[a];
		triangle.two = positions[b];
		triangle.three = positions[c];
		computeTriangleCenter(&triangle, &triangleCenter);
		subtract(&triangleCenter, &lightPosition, &lightDir);
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
			float time_float = ((float)(clock() - time_beg))/CLOCKS_PER_SEC;
			total_iter += time_float;
			time_beg = clock();
			for (int i = 0; i < 3; ++i){
				bool erased = false;
				if (edgesSet.erase(edges[i]) != 0) {
					erased = true;
				}
				if (edgesSet.erase(reverseEdges[i]) != 0) {
					erased = true;
				}
				if (not erased) {
					edgesSet.insert(edges[i]);
				}
			}
			time_float = ((float)(clock() - time_beg))/CLOCKS_PER_SEC;
			total_erase += time_float;
		}
	}
	// std::cout << "Total iter : " << total_iter << std::endl;
	// std::cout << "Total erase : " << total_erase << std::endl;
	std::unordered_set<Edge>::iterator it;
	int i = 0;
	for (it = edgesSet.begin(); it != edgesSet.end(); ++it) {
		returnEdges[i++] = *it;
	}
	*returnSize = edgesSet.size();
}

extern "C" {
	void findContourEdges(Vector* positions, int* indices, Vector* normals,
					       int sizeIndices, Vector lightPosition, Edge* returnEdges, int* returnSize)
	{
		findContourEdges2(positions, indices, normals, sizeIndices, lightPosition, returnEdges, returnSize);
	}
}

