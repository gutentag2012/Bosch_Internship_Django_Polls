# Entities Package

This package deals with the connection to the database. All the models that are supported are listed below,  
as well as the routes to access them.

## Models

This section shows all the models this package has responsibility over.

### Poll

This is the entity that contains the final question and the relation to the possible answers.  
It is connected to a User entity and has a start and end date that determines how long the poll is displayed.

### Poll Answer

This entity saves all possible answers to a specific poll. All votes for this answer are stored as a relation to  
the account that made the vote.

### Tag

This entity saves a specific category a poll can have. It is represented by a name and a color and holds a relation to
multiple Polls.