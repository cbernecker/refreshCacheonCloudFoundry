# Synchronize in-memory objects over multiple instances in IBM CLOUD Cloud Foundary .

 presented by [Christian Bernecker](https://www.linkedin.com/in/bernecker-christian-ba5ab4170/)

 [[https://github.com/cbernecker/refreshCacheonCloudFoundary/blob/master/img/Cloud Foundary.png|alt=Cloud Foundary]]

This is a short demo of how can you synchronize in-memory objects over multiple instances in IBM CLOUD Cloud Foundary Apps. When you use multiple instances in a IBM Cloud Foundary App (CF) and you use lists, arrays or objects to cache information in the memory you have to be careful with the refreshment of the cache. Because if you use an API Call to refresh the cache. Only the instances that the request hit will be updated. All others stayed in the same condition as before. Unfortunately there is no standard process designed in CF or IBM Cloud. Of course you can take a restart of your application. But if you have an application with a high availability this is not recommended.

There is a simple way to refresh the cache from the code side. You can access the following environment variables that contain the right information:

* CF_INSTANCE_INDEX
* VCAP_APPLICATION

the VCAP_APPLICATION contain the application_id that is needed to refresh the cache on all instances. Because you have to define the following http header to call a specific instance:

> -H "X-CF-APP-INSTANCE":"YOUR-APP-GUID:YOUR-INSTANCE-INDEX"

see: https://docs.cloudfoundry.org/concepts/http-routing.html#app-instance-routing

The idea is to let the instance that is hitted call all other exisiting instances. 

PSEUDO-CODE:

```Python
guid = os.gentenv(CF_INSTANCE_GUID)[application_id]
url = "https://" + os.gentenv(CF_INSTANCE_GUID)['application_uris'][0] + "/api/v1/refresh"

instance = 0
another_instance = True

while instance:
    try:
         payload = ""
         headers = {
                    'Content-Type': "application/json",
                    'X-CF-APP-INSTANCE': "guid :instance ",
                    'cache-control': "no-cache",
                    'Postman-Token': "c9a1b0c9-13a4-485e-bc2f-d530366c64dd"
                    }

           response = requests.request("GET", url, data=payload, headers=headers)
           instance += 1
    except:
        another_instance =False
```

## Prerequisites

* [Bluemix account](https://console.ng.bluemix.net/registration/)
* [Cloud Foundry CLI](https://github.com/cloudfoundry/cli#downloads)
* [Python](https://www.python.org/downloads/) - Version 3.6

## START


