#### Pinoy-Desk database as a service

     Pinoy-Desk Database as a Service is intended
     for you use by Pinoy Desk's Several applications
     hosted as microservices. in Google Cloud Platform.
 
 **How it Works?**
 --
     by creating API endpoints for databases hosted in Google Cloud Platform this service is able to 
     offer endpoints to access, save, and update data to services running in 
     Google Cloud Run and GCP Functions, and in the future can be expanded without affecting the 
     services depending on the databases being managed by this data-service.

   
 **What it Handles**
 --
 Presently the database can handle several services
   - ***Users***
   - ***Stocks***
   - ***Brokers***
   - ***Stock Exchanges***
   - ***API***
        - ***(Settings Database, & Temp Data )***
   - ***Scrapping*** 
        - ***(Settings Database, & Temp Data)***
   - ***Affiliates***
   - ***HelpDesk***
   - ***Memberships***
   - ***Stats***
--     
 ####Access to the our service is provided through: 
   - PubSub
   - HTTP Endpoints
 
 #### Catching Policy
    The database service will utilize aggressive caching to avoid multiple
    database searches for the same content on the datastore.
    
    This will be done in the following manner.
    --
    1. ***Through catching JSON Responses*** from database queries with Service Workers registered on Cloud Flare.     
        - The data-service is able to purge the cached data through an API call.
        - The Cache will expired through a predetermined time(TTL) if a purge was not triggered.
    2. Through Catching Requests for data on the browser through a service worker registered on each client browser.
        - The data stored maybe be purged from the back-end through push messages triggered events.
        - The data stored will expire when a cache TTL expires 
        - Cache TTL for both the CDN and the browser settings will be dynamically calculated by the 
        database service whenever a new request is made.
    
    3. Through Mem Cache on Client Servers Application, so as to avoid searching the database twice for the same info
    the client cache will also dynamically determine the Cache TTL, and also the data-service may 
    purge the cache through an API Call to the client server. thereby causing the client to fetch fresh data.         
    
     
         
                
    
      
    
 
 
 
 

