# Preparation

We will get the postman client operational and ready for use in the various sections of this lab. The first step will be to import the collections and environment into postman or pull them in from the publicly shared workspace.

## Collections

**Collections** are groupings of requests within postman. They are logical structures that allow requests to be grouped and run as a collection within Postman. Within this lab, we have built collections around specific use cases. Each collection can be exported and imported separately or together within a workspace. **Workspaces** are separate tenants within Postman and operate separately from each other. 

Within a **Workspace**, you may have multiple **Collections** and **Environments**. **Environments** utilize variables that are shared across multiple collections and requests. **Variables** can be localized to **Environments**, and **Collections**.

To give the use case a better flow, each API call has been built with **Tests** within **Test** scripts to explain what did or did not happen during the API call and to stop the flow in the event of an error. Secondarily the test script calls the next subsequent API call in the chain when using the **Collection Run** methodology.


[**Next Section**](./03-Postman.md)

[**Return to LAB Menu**](../README.md)