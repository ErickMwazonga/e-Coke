### e-Coke API Version 1.0
This is a documentation of all the REST endpoints exposed by e-Coke API.
Token based authentication, using JSON web tokens is required for accessing in
of the endpoints documented herein.

### Resources
1. Brands

### Brands
Soft drink brand information collected in a given location
##### Endpoints
1. POST `api/brands/create `- Create a single brand in the database.
2. GET `api/brands` - List all brands in the database.
3. GET `api/brands/{id}` - Get a single brand by its id.
4. PUT `api/brands/{id}/update` - Retrieve and update a single brand.
5. DELETE `api/brands/{id}/delete` - Delete a single brand from the database.
