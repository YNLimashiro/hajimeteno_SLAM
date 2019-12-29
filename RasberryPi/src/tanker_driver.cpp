#include "ros/ros.h"
#include "std_msgs/String.h"
#include "tanker_driver.h"
#include "tanker/input_keys.h"
#include <wiringPi.h>



#define L_IN1 24 
#define L_IN2 23 
#define L_PWM 18

#define R_IN1 12
#define R_IN2 16
#define R_PWM 20

#define STBY 25

using namespace std;

/*
node:tanker
topic:command
message:input_keys
*/


int main(int argc,char **argv){
  if(init_GPIO() == -1){
    return 0;
  }
  ros::init(argc,argv,"tanker");
  ros::NodeHandle nodeHandle;
  ros::Subscriber subscriber = nodeHandle.subscribe("command",10,driveCallback);
  ros::spin();
  
  return 0;

}


int init_GPIO(){
  if(wiringPiSetupGpio() == -1){
    return -1;
  }
  pinMode(L_IN1,OUTPUT);
  pinMode(L_IN2,OUTPUT);
  pinMode(L_PWM,OUTPUT);
  pinMode(R_IN1,OUTPUT);
  pinMode(R_IN2,OUTPUT);
  pinMode(R_PWM,OUTPUT);
  pinMode(STBY,OUTPUT);
 
  digitalWrite(STBY,1);
  
}

void driveCallback(const tanker::input_keys& msg){
  cout << "up:" << msg.up << endl;
  cout << "down:" << msg.down << endl;
  cout << "left:" << msg.left << endl;
  cout << "right:" << msg.right << endl;

  
  if(msg.right == 1){
    digitalWrite(L_IN1, 0);
    digitalWrite(L_IN2, 1);
    digitalWrite(L_PWM,1);
    digitalWrite(R_IN1, 1);
    digitalWrite(R_IN2, 0);
    digitalWrite(R_PWM,1);
    return;
  }else if(msg.left == 1){
    digitalWrite(L_IN1, 1);
    digitalWrite(L_IN2, 0);
    digitalWrite(L_PWM,1);
    digitalWrite(R_IN1, 0);
    digitalWrite(R_IN2, 1);
    digitalWrite(R_PWM,1);
    return;
  }else if(msg.up == 1){
    digitalWrite(L_IN1, 1);
    digitalWrite(L_IN2, 0);
    digitalWrite(L_PWM,1);
    digitalWrite(R_IN1, 1);
    digitalWrite(R_IN2, 0);
    digitalWrite(R_PWM,1);
    return;
  }else if(msg.down == 1){
    digitalWrite(L_IN1, 0);
    digitalWrite(L_IN2, 1);
    digitalWrite(L_PWM,1);
    digitalWrite(R_IN1, 0);
    digitalWrite(R_IN2, 1);
    digitalWrite(R_PWM,1);
    return;
  }else {
    digitalWrite(L_IN1, 0);
    digitalWrite(L_IN2, 0);
    digitalWrite(L_PWM,1);
    digitalWrite(R_IN1, 0);
    digitalWrite(R_IN2, 0);
    digitalWrite(R_PWM,1);
  }


  
}
