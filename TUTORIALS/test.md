<div style="display: flex; gap: 50px;">

  <div style="position: relative; width: 500px;">
    <svg width="100%" height="100%" viewBox="0 100 520 260" style="position: absolute; top: 0; left: 0; z-index: -1;">
      <rect x="10" y="10" width="500" height="440" rx="20" ry="20" style="fill:#333333;"/>
    </svg>
    <div style="padding: 20px; color: white; text-align: center;">
      <h2 style="margin-bottom: 30px;">Catalyst Center License Synchronization</h2>
      <p>Catalyst Center 2.3.7.X does not have a patch for synchronizing large inventories of devices with Cisco and times out. This bug is being addressed in 3.1 but in 2.3.7.x code is an issue.</p>
      <p>This python program utilizes the Catalyst Center Python SDK 3.1.3 to update the licensing and synchronize it with Cisco. Credentials need to be entered into the program, but it pulls the smart account information from catalyst center at run time. For scheduling purposes you could put this behind a cron job.</p>
      <p>The python lives in this location:</br>
      <a href="https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/CATC-TEMPLATES/raw/master/CODE/PYTHON/CATCLicenseSync.zip" style="color: lightblue;">**⬇︎Catalyst Center Licensing Synchronization⬇︎**</a></br></p>
      <p>There is a requirements file which they should use prior to trying this. It is working with python 3.9.2 and python sdk 3.1.3 with cat center 2.3.7.10</p>
    </div>
  </div>

  <div style="position: relative; width: 500px;">
    <svg width="100%" height="100%" viewBox="0 100 520 260" style="position: absolute; top: 0; left: 0; z-index: -1;">
      <rect x="10" y="10" width="500" height="440" rx="20" ry="20" style="fill:#333333;"/>
    </svg>
    <div style="padding: 20px; color: white; text-align: center;">
      <h2 style="margin-bottom: 30px;">Catalyst Center Telemetry Synchronization</h2>
      <p>After a Catalyst Center upgrade telemetry sometimes breaks or does not get updated on certain devices. To alleviate this, a python program can be run to fix all devices as this procedure is non-impacting.</p>
      <p>This python program utilizes the Catalyst Center Python SDK 3.1.3 to update the licensing and synchronize it with Cisco. Credentials need to be entered into the program. For scheduling purposes you could put this behind a cron job.</p>
      <p>The python lives in this location:</br>
      <a href="https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/CATC-TEMPLATES/raw/master/CODE/PYTHON/CATCTelemetrySync.zip" style="color: lightblue;">**⬇︎Catalyst Center Telemetry Synchronization⬇︎**</a></br></p>
      <p>There is a requirements file which they should use prior to trying this. It is working with python 3.9.2 and python sdk 3.1.3 with cat center 2.3.7.10</p>
    </div>
  </div>

</div>
