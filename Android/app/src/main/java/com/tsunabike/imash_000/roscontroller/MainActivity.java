package com.tsunabike.imash_000.roscontroller;


import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.hardware.Camera;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.MotionEvent;
import android.widget.Toast;


import com.google.common.collect.Lists;

import org.jboss.netty.buffer.ChannelBuffer;
import org.ros.address.InetAddressFactory;
import org.ros.android.BitmapFromCompressedImage;
import org.ros.android.MessageCallable;
import org.ros.android.RosActivity;
import org.ros.android.view.RosImageView;
import org.ros.android.view.RosTextView;
import org.ros.android.view.VirtualJoystickView;
import org.ros.android.view.camera.RosCameraPreviewView;
import org.ros.android.view.visualization.VisualizationView;
import org.ros.android.view.visualization.layer.CameraControlLayer;
import org.ros.android.view.visualization.layer.LaserScanLayer;
import org.ros.android.view.visualization.layer.Layer;
import org.ros.android.view.visualization.layer.OccupancyGridLayer;
import org.ros.android.view.visualization.layer.PathLayer;
import org.ros.android.view.visualization.layer.PosePublisherLayer;
import org.ros.android.view.visualization.layer.PoseSubscriberLayer;
import org.ros.android.view.visualization.layer.RobotLayer;
import org.ros.node.NodeConfiguration;
import org.ros.node.NodeMain;
import org.ros.node.NodeMainExecutor;

import java.io.IOException;

import sensor_msgs.CompressedImage;


public class MainActivity extends RosActivity {

    private VirtualJoystickView virtualJoystickView;
    private VisualizationView visualizationView;
    private RosTextView<std_msgs.String> rosTextView;
    private Talker talker;
    private int cameraId;
    private RosCameraPreviewView rosCameraPreviewView;
    private RosImageView<sensor_msgs.CompressedImage> image;

    public MainActivity() {
        super("Teleop", "Teleop");
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.settings_menu, menu);
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case R.id.virtual_joystick_snap:
                if (!item.isChecked()) {
                    item.setChecked(true);
                    virtualJoystickView.EnableSnapping();
                } else {
                    item.setChecked(false);
                    virtualJoystickView.DisableSnapping();
                }
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }

    @SuppressWarnings("unchecked")
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        virtualJoystickView = (VirtualJoystickView) findViewById(R.id.virtual_joystick);
        image = (RosImageView<sensor_msgs.CompressedImage>) findViewById(R.id.image);
        image.setTopicName("/webcam/image_raw/compressed");
        image.setMessageType(sensor_msgs.CompressedImage._TYPE);
        image.setMessageToBitmapCallable(new BitmapFromCompressedImage());

        /*rosTextView = (RosTextView<std_msgs.String>) findViewById(R.id.text);
        rosTextView.setTopicName("chatter");
        rosTextView.setMessageType(std_msgs.String._TYPE);
        rosTextView.setMessageToStringCallable(new MessageCallable<String, std_msgs.String>() {
            @Override
            public String call(std_msgs.String message) {
                return message.getData();
            }
        });
*/
        /*visualizationView = (VisualizationView) findViewById(R.id.visualization);
        visualizationView.getCamera().jumpToFrame("map");
        visualizationView.onCreate(Lists.<Layer>newArrayList(new CameraControlLayer(),
                new OccupancyGridLayer("map"), new PathLayer("move_base/NavfnROS/plan"), new PathLayer(
                        "move_base_dynamic/NavfnROS/plan"), new LaserScanLayer("base_scan"),
                new PoseSubscriberLayer("simple_waypoints_server/goal_pose"), new PosePublisherLayer(
                        "simple_waypoints_server/goal_pose"), new RobotLayer("base_footprint")));
*/

    }



    @Override
    protected void init(NodeMainExecutor nodeMainExecutor) {
        talker = new Talker();
        /*get Ros Server*/
        NodeConfiguration  nodeConfiguration =NodeConfiguration.newPublic(InetAddressFactory.newNonLoopback().getHostAddress(),getMasterUri());
        /* Create Node*/
        //nodeMainExecutor.execute(rosTextView, nodeConfiguration.setNodeName("rostextview"));
        //nodeMainExecutor.execute(talker, nodeConfiguration.setNodeName("talker"));
        nodeMainExecutor.execute(image, nodeConfiguration.setNodeName("android/video_view"));
        nodeMainExecutor.execute(virtualJoystickView, nodeConfiguration.setNodeName("virtual_joystick"));


    }

    @Override
    public void onDestroy(){
        super.onDestroy();
        nodeMainExecutorService.onDestroy();
        
    }

}