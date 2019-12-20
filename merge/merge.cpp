#include <pcl/io/ply_io.h>
#include <pcl/point_types.h>
#include <iostream>

using namespace std;
using namespace pcl;

int main(int argc, char** argv){
  PointCloud<PointXYZ>::Ptr cloud (new PointCloud<PointXYZ>);
  if(io::loadPLYFile<PointXYZ> (argv[1], *cloud) == -1){
    cout << "ERROR: couldn't find file" << endl;
    return (1);
  } else {
    cout << "loaded" << endl;
  }
  return 0;
}
