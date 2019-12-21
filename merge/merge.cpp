#include <pcl/io/ply_io.h>
#include <pcl/point_types.h>
#include <iostream>
#include <pcl/visualization/cloud_viewer.h>

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
  /*pcl::visualization::PCLVisualizer::Ptr viewer (new pcl::visualization::PCLVisualizer ("3D Viewer"));
  viewer->setBackgroundColor (0, 0, 0);
  viewer->addPointCloud<pcl::PointXYZ> (cloud, "sample cloud");
  viewer->setPointCloudRenderingProperties (pcl::visualization::PCL_VISUALIZER_POINT_SIZE, 1, "sample cloud");
  viewer->addCoordinateSystem (1.0);
  viewer->initCameraParameters ();*/
  cout <<*cloud << endl;
  return 0;
}
