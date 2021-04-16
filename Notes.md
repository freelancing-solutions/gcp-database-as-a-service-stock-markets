
End of day stock data for the phillipines
https://www.pseapi.com/


database manager will run as an 
app engine instance and expose API's
which will be utilized by GCP Functions

- Will manage database instances for
    - stocks
    - users
    - settings    
   
- Text from PDF Extractor
    - will run as GCP Function
    - read from settings api to get settings
    - store data on stocks
    - trigger is GCP Tasks - Scheduled in APP Engine     

- End of Day API for Philippine's Stock Exchange
    - will run as GCP Function
    - Gets triggered by a task from app engine
    - Tasks will be scheduled due to settings on the database
    
        
       
