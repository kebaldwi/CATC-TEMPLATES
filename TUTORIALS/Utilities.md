# Utilities [![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/kebaldwi/DNAC-TEMPLATES)

This section will includes various utilities developed for specific use cases with regard to Catalyst Center.

<div style="display: flex; align-items: flex-start; gap: 10px;">

<table style="border-collapse: collapse; width: 500px; border: 1px solid #ddd; border-radius: 10px; overflow: hidden;">
  <tr>
    <td style="padding: 20px; text-align: center; border: 1px solid #ddd; background-color: #333333;">

## Catalyst Center License Synchronization

Catalyst Center 2.3.7.X does not have a patch for synchronizing large inventories of devices with Cisco and times out. This bug is being addressed in 3.1 but in 2.3.7.x code is an issue.

This python program utilizes the Catalyst Center Python SDK 3.1.3 to update the licensing and synchronize it with Cisco. Credentials need to be entered into the program, but it pulls the smart account information from catalyst center at run time. for scheduling purposes you could put this behind a cron job.

The python lives in this location:</br> 
<a href="https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/PYTHON/CATCLicenseSync.zip">**⬇︎Catalyst Center Licensing Synchronization⬇︎**</a></br>


There is a requirements file which they should use prior to trying this. It is working with python 3.9.2 and python sdk 3.1.3 with cat center 2.3.7.10       
    </td>
  </tr>
</table>

<table style="border-collapse: collapse; width: 500px; border: 1px solid #ddd; border-radius: 10px; overflow: hidden;">
  <tr>
    <td style="padding: 20px; text-align: center; border: 1px solid #ddd; background-color: #333333;">

## Catalyst Center Telemetry Synchronization

After a Catalyst Center upgrade telemetry sometimes breaks or does not get updated on certain devices. To alleviate this python program can be run to fix all devices as this procedure is non impacting.

This python program utilizes the Catalyst Center Python SDK 3.1.3 to update the licensing and synchronize it with Cisco. Credentials need to be entered into the program. For scheduling purposes you could put this behind a cron job.

The python lives in this location:</br>
<a href="https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/PYTHON/CATCTelemetrySync.zip">**⬇︎Catalyst Center Telemetry Synchronization⬇︎**</a></br></br>

There is a requirements file which they should use prior to trying this. It is working with python 3.9.2 and python sdk 3.1.3 with cat center 2.3.7.10
    </td>
  </tr>
</table>

</div>

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Return to Main Menu**](../README.md)