/* 
  Uses the Bean's internal temperature sensor to setup an iBeacon
  Major ID is voltage of battery
  Minor ID is temperature

  Set the BeanName and UUID of the Bean to be the same in this sketch as you will be
  looking for these with the python script.
*/

void setup() {
  Serial.begin();
  Bean.enableConfigSave(false);
  Bean.setBeanName("A100");
}

void loop() {
  // Get the current ambient temperature in degrees Celsius with a range of -40 C to 87 C.
  int temperature = Bean.getTemperature();
  int voltage     = Bean.getBatteryVoltage();

  Bean.setBeaconParameters(0xA100, voltage, temperature);
  
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" C");
  
  Serial.print("Voltage: ");
  Serial.print(voltage);
  Serial.println(" v");
  
  # Broadcast for 5 seconds and sleep for 55 seconds
  # This may be a bit aggressive for battery life, drop as needed
  Bean.setBeaconEnable(true);
  Bean.sleep(5000);
  Bean.setBeaconEnable(false);
  Bean.sleep(55000);
}

