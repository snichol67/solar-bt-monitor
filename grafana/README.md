## Grafana Setup ##
Grafana is an open source library for visualizing data.  You can run grafana on your raspberry pi, just make sure you know which binary to download.  It's based on which ARM processor your particular Pi is running.  I've installed the ARM7 binaries successfully on my Raspberry Pi 3 Model B.  Check the details of your system to be sure.

- Install Grafana
    
    Check the [Grafana web site](https://grafana.com/grafana/download?platform=arm) for the latest version of their application.  The URL below may link to older versions.
    ```
    wget https://dl.grafana.com/enterprise/release/grafana-enterprise-8.2.3.linux-armv7.tar.gz
    tar -zxvf grafana-enterprise-8.2.3.linux-armv7.tar.gz
    rm grafana-6.5.3.linux-armv7.tar.gz
    mv grafana-6.5.3/ grafana/   
    ```
- Create the grafana.service file in /etc/systemd/system/grafana.service
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
- Set Up the Grafana Service
    ```
    sudo systemctl daemon-reload
    sudo systemctl start grafana
    sudo systemctl status grafana
    sudo systemctl enable grafana
    ```
    - After grafana is installed, go to http://192.168.1.XXX:3000
    - Default log in is username: admin, password: admin
      - You'll be promted to create a unique password for your installation
- After the rest of your installation is complete, you can set up your prometheus data source and import the solar-bt-monitor.json file as a dashboard into grafana
  - Once you have running on your Pi, should be able to add it as a data source to grafana
    - From the left hand navigation, hover over the Configuration (gear icon) menu and choose Data Sources
    - Choose Add data soruce
    - Set the data source name
      - The included dashboard expects a data source named **solarmonitor**, so unless you need it to be something different it might be best to stick with this
    - Under the HTTP section, set the URL to http://192.168.1.XXX:9090
    - Scroll to the bottom and select Save & Test
  - Now we can import the included dashboard `solar-bt-monitor.json`
    - From the navigation on the left, hover over the Create (+ icon) menu and choose Import
    - Locate the `solar-bt-monitor.json` file and let it import
    - Navigate to the dashboard and ensure that it is displaying your data from prometheus
    - Note that the dashboard also includes an alert that's set up to send a notification when the battery charge level goes below 26%.  
      - I have mine hooked up to an IFTTT notification so that I get an notification on my phone when this happens
      - You could set up something similar or use any other type of webhook notification, the options within grafana are pretty broad here so use what makes sense to you if you want that kind of notification


