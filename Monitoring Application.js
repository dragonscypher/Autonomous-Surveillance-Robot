import React, { useState, useEffect } from 'react';
import { Text, View, StyleSheet, Image } from 'react-native';
import ROSLIB from 'roslib';
import { openDatabase } from 'react-native-sqlite-storage';

const App = () => {
  const [map, setMap] = useState(null);
  const [objectPositions, setObjectPositions] = useState([]);
  const [surveillanceData, setSurveillanceData] = useState([]);
  const [ros, setRos] = useState(null);

  useEffect(() => {
    // Initialize ROSBridge connection
    const ros = new ROSLIB.Ros({
      url: 'ws://robot_ip:9090', // Replace with the actual robot's IP address
    });
    setRos(ros);

    // Initialize SQLite3 database
    const db = openDatabase({ name: 'surveillance_data.db', location: 'default' });

    // Subscribe to ROS topics
    const mapTopic = new ROSLIB.Topic({
      ros: ros,
      name: '/map',
      messageType: 'sensor_msgs/Image',
    });
    mapTopic.subscribe((mapMessage) => {
      setMap(mapMessage.data);
    });

    const objectPositionsTopic = new ROSLIB.Topic({
      ros: ros,
      name: '/object_positions',
      messageType: 'std_msgs/String',
    });
    objectPositionsTopic.subscribe((objectPositionsMessage) => {
      setObjectPositions(objectPositionsMessage.data.split(', '));
    });

    // Get the surveillance data from the database
    db.transaction((tx) => {
      tx.executeSql('SELECT * FROM surveillance_data', [], (tx, results) => {
        setSurveillanceData(results.rows.raw());
      });
    });

    // Handle ROSBridge connection errors
    ros.on('error', (error) => {
      console.error('Error connecting to ROS:', error);
    });

    return () => {
      // Cleanup ROSBridge subscriptions and connections
      ros.close();
    };
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Autonomous Surveillance Robot</Text>
      <Image source={{ uri: `data:image/png;base64,${map}` }} style={styles.map} />
      <Text style={styles.objectPositions}>Object Positions:</Text>
      <View style={styles.objectPositionsList}>
        {objectPositions.map((objectPosition, index) => (
          <Text key={index}>{objectPosition}</Text>
        ))}
      </View>
      <Text style={styles.surveillanceData}>Surveillance Data:</Text>
      <View style={styles.surveillanceDataList}>
        {surveillanceData.map((surveillanceDatum, index) => (
          <Text key={index}>{surveillanceDatum.timestamp}: {surveillanceDatum.object_class} at ({surveillanceDatum.x_position}, {surveillanceDatum.y_position}, {surveillanceDatum.z_position})</Text>
        ))}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  map: {
    width: 300,
    height: 300,
  },
  objectPositions: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  objectPositionsList: {
    marginTop: 10,
  },
  surveillanceData: {
    fontSize: 16,
    fontWeight: 'bold',
    marginTop: 10,
  },
  surveillanceDataList: {
    marginTop: 10,
  },
});

export default App;
