###Stocks EndPoint

- Admin App Microservice
    - access: HTTP API Calls
- GCP Functions
    - access: no access
    - reason: will use pubsub to send calls to this endpoint
- User APP Microservice
    - access: HTTP API Calls


##### Endpoints

/create stocks
    
    - /api/v1/stocks/create/stock
    - /api/v1/stocks/create/broker
    - /api/v1/stocks/create/stock-model
    - /api/v1/stocks/create/buy-volume
    - /api/v1/stocks/create/sell-volume
    - /api/v1/stocks/create/net-volume
    
/return all stocks method POST
    
    - /api/v1/all/stocks
    - /api/v1/all/brokers
    - /api/v1/all/stock-models
    
/daily stocks method POST
    
    - /api/v1/stocks/item/stock
    - /api/v1/stocks/item/broker
    - /api/v1/stocks/item/stock-model
    - /api/v1/stocks/item/buy-volume
    - /api/v1/stocks/item/sell-volume
    - /api/v1/stocks/item/net-volume
    
/day volumes method POST

    - /api/v1/stocks/day-volumes/buy-volumes
    - /api/v1/stocks/day-volumes/sell-volumes
    - /api/v1/stocks/day-volumes/net-volumes
        