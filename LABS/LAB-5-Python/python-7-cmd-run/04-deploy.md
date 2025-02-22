# Device Inventory Retrieval

## Pipeline Overview

In the previous step we pasted a **Groovy Script** into the **Pipeline Configuration**. This script tells Jenkins what to do when the **Pipeline** is initiated.

Let's examine the **Groovy Script** in more detail:

```GROOVY
pipeline {
    agent any

    stages {
        stage('Retrieve Device Inventory') {
            steps {
                script {
                    def previousModifiedTime = null
                    def currentModifiedTime = null

                    while (true) {
                        // Retrieve the previous modified time from a file or environment variable
                        println 'Monitoring Hierarchy Build for changes'
                        def storedModifiedTime = readFile('/root/DEVWKS-2176/timestamp/previous_modified_time_inventory.txt').trim()
                        if (storedModifiedTime) {
                            previousModifiedTime = storedModifiedTime.toLong()
                        }

                        // Check if any files exist in the subdirectory except placeholder.txt
                        def filesExist = sh(script: 'find /root/DEVWKS-2176 -type f -name "DNAC-Design-Settings.csv" | wc -l', returnStdout: true).trim().toInteger() > 0

                        if (filesExist) {
                            // Execute a shell command to retrieve the last modified timestamp of any files except placeholder.txt
                            def lastModifiedOutput = sh(script: 'find /root/DEVWKS-2176 -type f -name "DNAC-Design-Settings.csv" -exec stat -c %Y {} \\; | sort -n | tail -n 1', returnStdout: true).trim()
                            currentModifiedTime = lastModifiedOutput.toLong()
                            println "Current Timestamp: ${currentModifiedTime}"

                            if (previousModifiedTime == null || currentModifiedTime != previousModifiedTime) {
                                // Execute your desired steps or stages here
                                println 'Files changed'
                                dir('/root/DEVWKS-2176') {
                                    sh 'python3 /root/DEVWKS-2176/device_inventory.py'
                                }
                            } else {
                                println 'No changes'
                            }
                        } else {
                            println 'No files found in the subdirectory'
                        }

                        // Store the current modified time for future comparisons
                        writeFile file: '/root/DEVWKS-2176/timestamp/previous_modified_time_inventory.txt', text: currentModifiedTime.toString()
                        sleep 180
                    }
                }
            }
        }
    }

    post {
        cleanup {
            cleanWs()
        }
        always {
            echo '\n\nJenkins Device Inventory build end'
        }
    }
}
```

First thing we should note is that the indentation **does** matter with **Groovy Scripting**. Secondarily, it is important that when using various methods, the correct **Plugins** are installed. 

The way this script is generally designed to work is that when initiated it loops until you cancel it. Persistently it checks for changes in the **CSV** in the **directory** in the `/root/DEVWKS-2176/` and then gathers the **timestamp** from the **CSV** file and compares it to the previous collected **timestamp**. If the **timestamp** has **changed**, the file has been modified and the **Pipeline** automatically runs the **Python** program to **retrieve** the **Inventory** from Cisco Catalyst Center.

## Retrieve Inventory Pipeline Build

We will now **retrieve** the **inventory** as previously discussed.

Follow these steps:

1. Ensure the previous pipeline **DNAC-Templates** is **stopped** and not running, if not **stop** it.

2. Navigate and open the desired **Pipeline** within the **Jenkins Dashboard**:

   ![json](./images/Jenkins_Dashboard_2.png?raw=true "Import JSON")

3. Click **Build** 

   ![json](./images/Jenkins_Item_Inventory_Dashboard.png?raw=true "import JSON")

4. To observe the **Pipeline** run of the programs, do the following:

   1. Click on the most recent small number in the **Build History** 

   ![json](./images/Jenkins_Item_Inventory_Build.png?raw=true "Import JSON")

   2. Within that window click on **Console Output**

5. To stop the **Pipeline** click the small red X in the **top right** of either the **Build** or the **Build History Number**

      ![json](./images/Jenkins_Item_Inventory_console.png?raw=true "Import JSON")
      ![json](./images/Jenkins_Item_Inventory_console2.png?raw=true "Import JSON")
      
> [**Next Section**](./05-verify.md)
