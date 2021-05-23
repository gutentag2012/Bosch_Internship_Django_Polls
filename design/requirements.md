# Requirements

The requirements listed in this document shall be implemented and tested to an extend that satisfies the described
meters.

## Users / Login

| ID          | M001                                                                     |
| ----------- | ------------------------------------------------------------------------ |
| Description | A user shall only be able to send request to the system if authenticated |
| Meter       | Test requests with and without login                                     |

| ID          | M002                                                        |
| ----------- | ----------------------------------------------------------- |
| Description | Only registered users shall be able to log into the system  |
| Meter       | Log in with credentials that are not stored in the database |

| ID          | M003                                                      |
| ----------- | --------------------------------------------------------- |
| Description | Polls and votes shall be stored relative to a user        |
| Meter       | Create a poll and vote on a poll, then check the database |

## Persistence

| ID          | M004                                                      |
| ----------- | --------------------------------------------------------- |
| Description | Every newly created data shall be saved into the database |
| Meter       | Create an entity and check the database                   |

| ID          | M005                                                   |
| ----------- | ------------------------------------------------------ |
| Description | Only the most recent data shall be displayed to a user |
| Meter       | Edit data in the database and revisit the application  |

## Functionality

| ID          | M006                                                    |
| ----------- | ------------------------------------------------------- |
| Description | A user shall only be able to vote once on the same poll |
| Meter       | Vote on a poll and try to vote another time             |

| ID          | M007                                                                  |
| ----------- | --------------------------------------------------------------------- |
| Description | The results of a poll shall only be displayed after the vote was send |
| Meter       | Check the application before sending a vote                           |
