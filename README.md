# Solar Bluetooth Monitor
Python app to read data from Renogy solar Charge Controllers using the [BT-1](https://www.renogy.com/bt-1-bluetooth-module-new-version/) bluetooth adapter. Personally tested with my **Rover 40A Charge Controller**. May also work with Renogy **Wanderer** series charge controllers.  My setup uses a **Raspberry Pi 3B+**. It might also work with other  "SRNE like" devices like Rich Solar, PowMr, WEIZE etc.

This setup uses prometheus for logging data and leverages grafana to create a real-time dashboard for monitoring the performance of your system.  The cheat sheet below contains some of my notes for setting up the system and getting the logging working.

# Solar Shed Cheat Sheet
This is my cheat sheet for setting up a workable version of this application.

1. Set up an SD card to run raspberry pi with the [instructions here](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/2).

    The easiest way to do this is to download the Raspberry Pi Imager app. You'll choose the default Raspberry Pi install, select your SD card, and when it's done, you'll have a fully bootable SD card.
2. Run raspi-config
    ```
    sudo raspi-config
    ```
   - Interface Options -> Enable SSH
   - Interface Options -> Enable VNC
   - System Options -> Hostname
     - Set a familiar name that you can then reference on your local netork (i.e. solar-monitor)
     - Once this is setup you can reference your device with a url like http://solar-monitor.local instead of its IP address
3. Run the following commands to update the system software:
    ```
    sudo apt-get update
    sudo apt-get upgrade
    ```

4. Install Prometheus
    
    Check the [prometheus web site](https://prometheus.io/download/) for the latest version of their application.  The URL below may link to older versions.
    ```
    wget https://github.com/prometheus/prometheus/releases/download/v2.31.1/prometheus-2.31.1.linux-armv7.tar.gz
    tar xfz prometheus-2.31.1.linux-armv7.tar.gz
    rm xfz prometheus-2.31.1.linux-armv7.tar.gz
    mv prometheus-2.31.1.linux-armv7.tar.gz prometheus
    ```
5. Copy the file in this project (`prometheus\prometheus.yml`) into the promethus install folder (`~/prometheus/prometheus.yml`), overwriting the existing file:
   ```
   cp ~/solar-bt-monitor/prometheus/prometheus.yml ~/prometheus/prometheus.yml
   ```

6. Create the prometheus.service file in /etc/systemd/system/prometheus.service
    ```
    [Unit]
    Description=Prometheus Server
    Documentation=https://prometheus.io/docs/introduction/overview/
    After=network-online.target

    [Service]
    User=pi
    Restart=on-failure

    #Change this line if Prometheus is somewhere different
    ExecStart=/home/pi/prometheus/prometheus \
    --config.file=/home/pi/prometheus/prometheus.yml \
    --storage.tsdb.path=/home/pi/prometheus/data

    [Install]
    WantedBy=multi-user.target
    ```
7. Setup the Prometheus Service
    ```
    sudo systemctl daemon-reload
    sudo systemctl start prometheus
    sudo systemctl status prometheus
    sudo systemctl enable prometheus
    ```
    - Verify Prometheus is running (modify the address below with the IP address of your Raspberry Pi)
        - http://192.168.1.XXX-v2:9090
8. Install Grafana
    
    Check the [Grafana web site](https://grafana.com/grafana/download) for the latest version of their application.  The URL below may link to older versions.
    ```
    wget https://dl.grafana.com/enterprise/release/grafana-enterprise-8.2.3.linux-armv7.tar.gz
    tar -zxvf grafana-enterprise-8.2.3.linux-armv7.tar.gz
    rm grafana-6.5.3.linux-armv7.tar.gz
    mv grafana-6.5.3/ grafana/   
    ```
9. Create the grafana.service file in /etc/systemd/system/grafana.service
    ```
    [Unit]
    Description=Grafana Server
    After=network.target

    [Service]
    Type=simple
    User=pi
    ExecStart=/home/pi/grafana/bin/grafana-server
    WorkingDirectory=/home/pi/grafana/
    Restart=always
    RestartSec=10

    [Install]
    WantedBy=multi-user.target
    ```
10. Set Up the Grafana Service
    ```
    sudo systemctl daemon-reload
    sudo systemctl start grafana
    sudo systemctl status grafana
    sudo systemctl enable grafana
    ```
    - After grafana is installed, go to http://192.168.1.XXX:3000
    - Default log in is username: admin, password: admin
      - You'll be promted to create a unique password for your installation


11. Install this project on your Raspberry Pi - https://github.com/snichol67/solar-bt-monitor.git
    ```
    cd ~/
    git clone https://github.com/snichol67/solar-bt-monitor.git
    cd solar-bt-monitor
    cp solar-monitor.ini.dist solar-monitor.ini
    ```
    
    - Install the GATT library
        ```
        pip install gatt
        ```
    - Install libscrc
        I had to build libscrc because it's not installable with pip3
        ```
        git clone https://github.com/hex-in/libscrc
        cd libscrc/
        python3 setup.py build
        sudo python3 setup.py install
        ```
    
    Now you'll need to edit the solar-monitor.ini with the specifics of your setup. You need to get the MAC address of your particular BT-1 device.  You can use a BLE scanner app like:
      - [BLE Scanner (Apple App Store)](https://apps.apple.com/us/app/ble-scanner-4-0/id1221763603)
      - [BLE Scanner (Google Play)](https://play.google.com/store/apps/details?id=com.macdom.ble.blescanner)
    
    Look for devices with alias `BT-TH-XXXX..`.  If the device doesn't show up in the scanner, make sure you force quit any of the Renogy apps that might be connected to your BT-1.

    After you've created the solar-monitor.ini file, it's time to test it out:
    ```
    cd ~/solar-bt-monitor
    ./solar-monitor.py
    ```

    The script will attempt to connect to your BT-1.  Often times, the bluetooth libraries will immediately disconnect. This script is set up by default to reconnect if that happens. Usually after 3-4 reconnect attempts, the application will connect and you'll see the values output on the console.

    The script by default logs the data read from the controller to prometheus. If prometheus is running on your pi, you should be able to go to the URL http://192.168.1.XXX:5000 and see some output that looks something like the following (you'll likely see a bunch of additional parameters).
    ```
    # HELP solarshed_battery_percentage Battery %
    # TYPE solarshed_battery_percentage gauge
    solarshed_battery_percentage 100.0
    # HELP solarshed_battery_volts Battery Voltage
    # TYPE solarshed_battery_volts gauge
    solarshed_battery_volts 13.600000000000001
    # HELP solarshed_battery_current Battery Current
    # TYPE solarshed_battery_current gauge
    solarshed_battery_current 5.5
    # HELP solarshed_controller_temperature_celsius Controller Temperature
    # TYPE solarshed_controller_temperature_celsius gauge
    solarshed_controller_temperature_celsius 32.0
    # HELP solarshed_battery_temperature_celsius Battery Temperature
    # TYPE solarshed_battery_temperature_celsius gauge
    solarshed_battery_temperature_celsius 25.0
    # HELP solarshed_load_volts Load Voltage
    # TYPE solarshed_load_volts gauge
    solarshed_load_volts 13.600000000000001
    # HELP solarshed_load_amperes Load Current
    # TYPE solarshed_load_amperes gauge
    solarshed_load_amperes 0.15
    # HELP solarshed_load_power_watts Load Power
    # TYPE solarshed_load_power_watts gauge
    solarshed_load_power_watts 2.0
    ...
    ```
12. Configure Grafana

    Now that you're logging data to prometheus, we need to set up grafana to use the this data source to display an awesome dashboard!

    - Go to your grafana install at http://192.168.1.XXX:3000 and log in.
    - Set up the grafana data source coming from prometheus 
      - From the navigation bar running down the left side of the window, select:
        - (Configuration (gear icon) -> Data Sources
        - Give the data source a good name (solar-monitor)
        - Under the HTTP section, set the URL to http://192.168.1.XXX:9090
        - Scroll to the bottom and select Save & Test
    -  From the Create menu (+ icon on left navigation panel), choose Import and import the example dashboard json file included in the grafana folder in this project


## References
This project borrows some of the best elements from the following projects.  It certainly wouldn't be possible without the work done on these projects.
 - [Olen/solar-monitor](https://github.com/Olen/solar-monitor)
 - [cyrils/renogy-bt1](https://github.com/cyrils/renogy-bt1)
 - [corbinbs/solarshed](https://github.com/corbinbs/solarshed)
 - [Rover 20A/40A Charge Controller—MODBUS Protocol](https://docs.google.com/document/d/1OSW3gluYNK8d_gSz4Bk89LMQ4ZrzjQY6/edit)
