//
// Created by yutaro on 19/12/05.
//
#include "ros/ros.h"
#include "std_msgs/String.h"
#include <tanker/driver.h>
#include <sstream>
#include <iostream>
using namespace std;


int main(int argc, char **argv){
  ros::init(argc,argv,"publisher");
  ros::NodeHandle nodeHandle;
  ros::Publisher publisher = nodeHandle.advertise<tanker::driver>("drive",10);
  ros::Rate loop_rate(10);
  string s;
  cin >> s;
  cout << s << endl;

  while (ros::ok()){
    tanker::driver driver;
    driver.forward = "f";
    driver.back = "b";
    driver.right = "r";
    driver.left = "l";
    ROS_INFO("publish: %s", driver.forward.c_str());
    publisher.publish(driver);

    ros::spinOnce();
    loop_rate.sleep();
  }
  return 0;
}
