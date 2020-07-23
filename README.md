# Flask-Task

## Functions
  ```
    homeDirectory() => Entry Point 
    
    searchByName() => Invoked by the search button, fetch data from APIs and contruct the table
    
    getSpeciesNameSpan() => Gets the Specie name from the provided URL and Calculate the average LifeSpan 
    
    getHomePlanet() => Gets the Home Planet name from the provided URL
    
    getMoviesList() => Gets the Movie List from the provided URL
  
  ```
  
  ## Classes
  ```
  Class ListItem => Contain get functions and table attributes 
  ```

  ## Test
Test can by run by the following command 
  ```
      python test_app.py
  ```
consist of 2 test functions
  ```
      test_search() => Validate that swapi returns a response
      test_ListItem() => Validate that all records in the customized list has value
  ```
