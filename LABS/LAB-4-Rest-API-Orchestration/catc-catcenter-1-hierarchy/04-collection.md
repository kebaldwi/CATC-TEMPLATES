# Hierarchy Build Collection

Postman is a powerful tool for editing and creating REST-API calls and allows us to utilize several features to accomplish everyday tasks. In this section of the tutorial, we will use a simple REST-API set, which has been grouped into a Postman Collection.

## Collections

Collections are groupings of API, which allow us to have workflows defined for specific tasks. 

### Open the collection

To investigate this collection, follow these steps:

Navigate and open the Collection through the following steps:

   1. Within Postman, click on the Collection shortcut in the sidebar
   2. Expand the collection `Catalyst Center API LAB 100 - Build Hierarchy` by clicking the arrow.
   3. The tab with the API within the collection will appear to the right
   4. You can view the configuration of the API through these tabs. As a quick reference, a green dot appears wherever configuration is applied.
   
      ![Request Paramaters](./assets/Postman-Collection-Token-Begin.png?raw=true)

## About the API

Within the API, you will notice the following:

   1. The method **POST** is used for this API
   2. The URL *https://***{{CCip}}***/dna/system/api/v1/auth/token* where the Environmental variable **{{CCip}}** holds the actual IP. Hover briefly over the variable to display the current data.

### Variables

There are three types of variables within Postman.

1. **Global** Variables available to **all requests** available in the Postman console **regardless of which collection** they belong
2. **Environment** Variables these are populated by the Environment and are used **across multiple Collections**
3. **Collection** Variables these are used across multiple Requests **within** a **specific Collection**
4. **Local** Variables are **temporary** and only accessible in your request scripts and are not available when the run is complete
5. **Data** Variables provide a data set in the form of JSON or CSV that is the user-supplied **data file**

### Authorization parameters

Click the `Authorization` tab to display the Authorization parameters

   1. Here, we see that this API is using **Basic Auth** to get a TOKEN
   2. Two environmental variables **{{CCuser}}** and **{{CCpwd}}** are used and can be viewed by checking show password, and hovering over the variables presented. The values are pulled from the environment variables.

      ![Request Authorization](./assets/Postman-Collection-Token-Auth.png?raw=true)

### Headers

Within the API, we will investigate the `Headers` through the following:

   1. Click the `Headers` tab to display the Header parameters:
   2. The API is using the **Content-Type** `application/json`

      ![Request Header](./assets/Postman-Collection-Token-Header.png?raw=true)

### Tests

Within the API, we will investigate the post response scripts formerly `Tests` through the following:

   1. Click the `Tests` or on the newer UI `Scripts` tab and select `Post Response` to display the Test parameters:

      ![Request Test Script](./assets/Postman-Collection-Token-Test.png?raw=true)
   
   2. The API has the following defined:

      ``` js
       1.     var jsonData = JSON.parse(responseBody);
       2.     if (jsonData.Token) {
       3.       pm.test("Token acquired",() => {pm.expect(pm.response.text()).to.include("Token");});
       4.       postman.setEnvironmentVariable("TOKEN", jsonData["Token"]); 
       5.     }
       6.     else {
       7.       pm.test("Token not acquired",() => {pm.expect(pm.response.text()).to.include("Token");});
       8.       postman.setNextRequest("null");
       9.     }
       10.    postman.setNextRequest("Get SiteIDs PreCheck")
      ```

      * Line 1 loads the response from the API and into a variable `jsonDATA`.
      * In line 2, we begin a conditional `if` statement to determine if the JSON response contains a field called `Token` with a token in it.
      * Within the `if` condition in line 4, we load the Token from the field within the JSON response into the environmental variable.
      * The end of the code block calls for the next API within the collection.

> [**Next Section**](./05-deploy.md)

> [**Return to LAB Menu**](../README.md)