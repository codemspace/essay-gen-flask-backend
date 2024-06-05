# Flask Backend

## Signin
```
POST : /api/v1/auth/signin
Request Body : 
        {
            "email": "admin@gmail.com",
            "password": "star123!@#"
        }
Response Body : 
        {
            "message": "User Sign In Successful",
            "status": true,
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MTU1Nzk0MDUsImV4cCI6MTcxNTU4MzAwNSwidXNlcl9pZCI6IjEiLCJmaXJzdG5hbWUiOiJBZG1pbiIsImxhc3RuYW1lIjoiVXNlciIsImVtYWlsIjoiYWRtaW5AZ21haWwuY29tIn0.Wx2RoqZkCkpdAG1mj-ii2lWVCAZikGJTe0grK7Zuvxk"
        }
```

## Signup
```
POST : /api/v1/auth/signup
Request Body : 
        {
            "email": "admin@gmail.com",
            "password": "star123!@#",
            "firstname": "Jhon",
            "lastname": "Doe"
        }
Response Body : 
        {
            "message": "User Sign up Successful",
            "status": true,
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MTU1NzkzMjEsImV4cCI6MTcxNTU4MjkyMSwidXNlcl9pZCI6IjEiLCJmaXJzdG5hbWUiOiJBZG1pbiIsImxhc3RuYW1lIjoiVXNlciIsImVtYWlsIjoiYWRtaW5AZ21haWwuY29tIn0.9fjvXPrWqPBteKUkrocxCkdoVoz7XsjfE56Y-Bt0GWA"
        }
```

## Google Auth
```
POST : /api/v1/auth/google
Request Body : 
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MTU1NzkzMjEsImV4cCI6MTcxNTU4MjkyMSwidXNlcl9pZCI6IjEiLCJmaXJzdG5hbWUiOiJBZG1pbiIsImxhc3RuYW1lIjoiVXNlciIsImVtYWlsIjoiYWRtaW5AZ21haWwuY29tIn0.9fjvXPrWqPBteKUkrocxCkdoVoz7XsjfE56Y-Bt0GWA"
        }
Response Body : 
        {
            "message": "Google Login Successful",
            "status": true,
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MTU1NzkzMjEsImV4cCI6MTcxNTU4MjkyMSwidXNlcl9pZCI6IjEiLCJmaXJzdG5hbWUiOiJBZG1pbiIsImxhc3RuYW1lIjoiVXNlciIsImVtYWlsIjoiYWRtaW5AZ21haWwuY29tIn0.9fjvXPrWqPBteKUkrocxCkdoVoz7XsjfE56Y-Bt0GWA"
        }
```

## Get Authenticated User
```
GET : /api/v1/auth/current-user
Response Body : 
        {
            "status": True,
            "data": {
                "user": {
                    "email": "admin@gmail.com",
                    "firstname": "Lion",
                    "lastname": "King",
                    "plan": {
                        "type": "UNLIMITED",
                        "renewalType": "month",
                        "nextPaymentDate": "2024-06-14",
                        "quotaUsage": 0
                    }
                }
            }
        }
```

## Subscription Create Checkout Session
```
POST : /api/v1/subscriptions/create-checkout-session
Request Body : 
        {
            "priceType": "monthly"
        }
Response Body : 
        {
            "status": True,
            "data": {
                "sessionId": "cs_test_a1KqOMVaXIXwvovtFAqYcoDgHFCvVOBu3iCQrsRfEOpWlitjuEhhErTEbh"
            }
        }
```

## Subscription Subscription success
```
POST : /api/v1/subscriptions/success
Request Body : 
        {
            "sessionId": "cs_test_a1KqOMVaXIXwvovtFAqYcoDgHFCvVOBu3iCQrsRfEOpWlitjuEhhErTEbh"
        }
Response Body : 
        {
            "status": True
        }
```

## Get document by Id
```
GET : /api/v1/documents/{document_id}
Response Body :
        {
            "status": True,
            "data": {
                "essay": "{essay_data}"
            }
        }
```

## Delete document by Id
```
DELETE : /api/v1/documents/{document_id}
Response Body :
        {
            "status": True,
            "message": "{message}"
        }
```

## Export document by Id
```
POST : /api/v1/documents/{document_id}/export
Request Body :
        {
            "type": "{type}" # "PDF", "DOC"
        }
```

## Get documents
```
GET : /api/v1/documents
Response Body :
        {
            "status": True,
            "data": {
                "documents": [
                    {
                        "id": 3,
                        "title": "{title}"
                    }
                ]
            }
        }
```