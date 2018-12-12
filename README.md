# Synchronize in-memory objects over multiple instances in IBM CLOUD Cloud Foundary Apps.

 presented by [Christian Bernecker](https://www.linkedin.com/in/bernecker-christian-ba5ab4170/)

![Cloud Foundary](https://github.com/cbernecker/refreshCacheonCloudFoundary/blob/master/img/Cloud%20Foundary.png)

This is a short demo of how can you synchronize in-memory objects over multiple instances in IBM CLOUD Cloud Foundary Apps. When you use multiple instances in a IBM Cloud Foundary App (CF) and you use lists, arrays or objects to cache information in the memory you have to be careful with the refreshment of the cache. Because if you use an API Call to refresh the cache. Only the instances that the request hit will be updated. All others stayed in the same condition as before. That means each instance has indepentend memory and they are not synchronized. Unfortunately there is no standard process designed in CF or IBM Cloud. Of course you can take a restart of your application. But if you have an application with a high availability this is not recommended.

# The Problem

### Initiated Cache after restart (synched)
![Iniate the cache](https://github.com/cbernecker/refreshCacheonCloudFoundary/blob/master/img/Iniated%20Cache.PNG)

### API Call to one of the instances 
![Update Cache](https://github.com/cbernecker/refreshCacheonCloudFoundary/blob/master/img/Updating%20Cache.PNG)

## Update the cache only on one Instacne (out of snych)
![Not Synched](https://github.com/cbernecker/refreshCacheonCloudFoundary/blob/master/img/NotSynched.PNG)


# The Solution

There is a simple way to refresh the cache from the code side. You can access the following environment variables that contain the right information:

* CF_INSTANCE_INDEX
* VCAP_APPLICATION

the VCAP_APPLICATION contain the application_id that is needed to refresh the cache on all instances. Because you have to define the following http header to call a specific instance:

> -H "X-CF-APP-INSTANCE":"YOUR-APP-GUID:YOUR-INSTANCE-INDEX"

see: https://docs.cloudfoundry.org/concepts/http-routing.html#app-instance-routing

The idea is to let the instance that is hitted call all other exisiting instances. 

### PSEUDO-CODE:

```Python
guid = os.gentenv(VCAP_APPLICATION)['application_id']
url = "https://" + os.gentenv(VCAP_APPLICATION)['application_uris'][0] + "/api/v1/refresh"

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

1. Clone the Repo or Download the Code
2. Create an CF instance on your IBM Cloud Account. You can do that very easily with the following command: 

> cf push 

these command push an app called Python-Refresh-Cache-Multiple-Instances to your IBM Cloud Account that has 3 Instances running with 128MB. It looks like:

![Push](https://github.com/cbernecker/refreshCacheonCloudFoundary/blob/master/img/Push.PNG)

3. Note the url
4. You can use the following API Calls:

|URL                         | Description                                                      |      |
|----------------------------|------------------------------------------------------------------|------|
| http://url/api/v1/current  | Shows the current cached Object and the instance that is called  | POST |
| http://url/api/v1/update   | You can update the cahced object on the instance this is hitted  | POST |
| http://url/api/v1/refresh  | With refresh you can uptade the object over all instances        | POST |

5. If you call http://url/api/v1/update with the body 

```JSON 
{
    "MY_CACHE": "NEW_OBJECT2"
}
```

you will receive
```JSON 
{
    "Cache Object": {
        "MY_CACHE1": "OBJECT1",
        "MY_CACHE2": "OBJECT2",
        "MY_CACHE3": "NEW_OBJECT2"
    },
    "Instance": "0"
}
```

6. Now call http://url/api/v1/current many times and check what is in the cache of instance one and two.
7. If you call http://url/api/v1/refresh with the body 

```JSON 
{
    "MY_CACHE": "NEW_OBJECT2"
}
```
8. Go to step 6 and check if all instances are updated 


PERFEKT YOU GOT IT. Go now to the code and check how it works!!!!



