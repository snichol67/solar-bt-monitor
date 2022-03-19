# Solar Bluetooth Monitor
Python app to read data from Renogy solar Charge Controllers using the [BT-1](https://www.renogy.com/bt-1-bluetooth-module-new-version/) bluetooth adapter. Personally tested with my **Rover 40A Charge Controller**. May also work with Renogy **Wanderer** series charge controllers.  My setup uses a **Raspberry Pi 3B+**. It might also work with other  "SRNE like" devices like Rich Solar, PowMr, WEIZE etc.

This setup uses prometheus for logging data and leverages grafana to create a real-time dashboard for monitoring the performance of your system.  The cheat sheet below contains some of my notes for setting up the system and getting the logging working.

# Solar Shed Cheat Sheet
This is my cheat sheet for setting up a workable version of this application.

1. Set up an SD card to run raspberry pi(https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/2)
2. Run raspi-config
   - Enable SSH
   - Enable VNC
   - Set the Host Name
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
5. Set up prometheus.yml file in ~/prometheus/prometheus.yml:
    ```
    # my global config
    global:
    scrape_interval: 15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
    evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
    # scrape_timeout is set to the global default (10s).

    # Alertmanager configuration
    alerting:
    alertmanagers:
        - static_configs:
            - targets:
            # - alertmanager:9093

    # Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
    rule_files:
    # - "first_rules.yml"
    # - "second_rules.yml"

    # A scrape configuration containing exactly one endpoint to scrape:
    # Here it's Prometheus itself.
    scrape_configs:
    # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
    - job_name: "solarshed"

        # metrics_path defaults to '/metrics'
        # scheme defaults to 'http'.

        static_configs:
        - targets: ["localhost:5000"]

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
    1. After grafana is installed, go to http://192.168.1.132:3000
    2. Default log in is admin/admin
    3. From the Create menu (+ icon on left navigation panel), choose Import and import the dashboard json file
    4. Set up a data source from prometheus (Configuration (gear icon) -> Data Sources
       1. Our configuration should be http://192.168.1.132:9090


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
    
    Look for a devices with alias `BT-TH-XXXX..`.  If the device doesn't show up in the scanner, make sure you force quit any of the Renogy apps that might be connected to your BT-1.

## Dependencies

```
gatt
libscrc
```

## References

 - [Olen/solar-monitor](https://github.com/Olen/solar-monitor)
 - [cyrils/renogy-bt1](https://github.com/cyrils/renogy-bt1)
 - [corbinbs/solarshed](https://github.com/corbinbs/solarshed)
 - [Rover 20A/40A Charge Controller—MODBUS Protocol](https://docs.google.com/document/d/1OSW3gluYNK8d_gSz4Bk89LMQ4ZrzjQY6/edit)
