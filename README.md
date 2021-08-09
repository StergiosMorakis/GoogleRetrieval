# Information Retrieval Project

***

A script for collecting empirical evidence on Google search engine's bias when ranking its results, measured with Jaccard distance and Kendall rank correlation.

***

### Experimental procedure

- topic
- **Sub** query 1
- **Main** query 1
- **Sub** query 2
- **Main** query 2

    User 1 queries main-query 1, waits 30 minutes and then queries sub-query 2s followed by main-query 2. After 30 minutes (restarting Google session), user 2 queries main-query 2, waits 30 minutes and then queries sub-query 1, followed by main-query 1. This procedure is repeated on a variety of topics.


### Requirements

- Chrome or Mozilla webdriver

### Author

*Stergios Morakis*