#include "ros/ros.h"
#include "std_msgs/String.h"
#include "tanker_driver.h"
#include "tanker/input_keys.h"

using namespace std;

/*
node:tanker
topic:command
message:input_keys
*/


int main(int argc,char **argv){
  ros::init(argc,argv,"tanker");
  ros::NodeHandle nodeHandle;
  ros::Subscriber subscriber = nodeHandle.subscribe("command",10,driveCallback);
  ros::spin();
  return 0;

}


void driveCallback(const tanker::input_keys& msg){
  cout << "up:" << msg.up << endl;
  cout << "down:" << msg.down << endl;
  cout << "left:" << msg.left << endl;
  cout << "right:" << msg.right << endl;
}
