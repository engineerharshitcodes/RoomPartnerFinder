# Room Partner Finder

A distributed **Room Partner Finder** backend built with **Python Flask**, **MongoDB**, and an **AI/ML-based compatibility matching system**.

The application supports two types of users:

1. **Room Owner** – users who have a room/property available and are looking for a suitable partner.
2. **Partner Seeker** – users who are searching for a room and a compatible roommate/partner.

The project is designed to demonstrate practical concepts from **Distributed Databases, NoSQL databases, REST APIs, and Machine Learning**.

---

## 1. Project Objectives

The main objectives of the project are:

- Provide separate authentication for Room Owners and Partner Seekers.
- Allow Room Owners to publish and manage available rooms.
- Allow Partner Seekers to create detailed roommate profiles.
- Search rooms and potential partners using filters.
- Calculate roommate compatibility using AI/ML techniques.
- Use MongoDB as the NoSQL database.
- Demonstrate distributed database concepts such as:
  - Horizontal fragmentation
  - Sharding
  - Replication
  - Data distribution
  - Distributed queries
  - Fault tolerance
  - Scalability
- Provide REST APIs that can be tested using Postman.
- Keep the architecture modular so a React frontend can be connected later.

---

## 2. High-Level Architecture

```text
                         FRONTEND
                    React / HTML / JS
                           |
                           v
                  +------------------+
                  |    Flask API     |
                  |     Backend      |
                  +--------+---------+
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
       Authentication   Room APIs    Matching APIs
             |             |             |
             +-------------+-------------+
                           |
                           v
                 +-------------------+
                 |   MongoDB Cluster  |
                 +---------+---------+
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
          Shard 1       Shard 2       Shard 3
          Delhi         Noida         Gurgaon
             |             |             |
             +-------------+-------------+
                           |
                           v
                  +----------------+
                  |   AI/ML Engine |
                  | Compatibility  |
                  +----------------+
```

---

## 3. User Roles

### 3.1 Room Owner

A Room Owner can:

- Register and login.
- Add a room.
- Update room information.
- Delete a room.
- Set rent and location.
- Specify room type and facilities.
- Specify preferred roommate characteristics.
- View compatible Partner Seekers.
- Accept or reject partner requests.

Example:

```text
Name: Rahul
City: Delhi
Area: Rohini
Rent: ₹10,000
Room Type: 2BHK

Preferred Partner:
Age: 20-27
Occupation: Student
Smoking: No
Food: Vegetarian
Cleanliness: High
```

### 3.2 Partner Seeker

A Partner Seeker can:

- Register and login.
- Create a roommate profile.
- Specify budget.
- Specify preferred location.
- Specify lifestyle preferences.
- Search available rooms.
- View compatibility scores.
- View recommended partners.
- Send partner requests.
- Track request status.

Example:

```text
Name: Aman
Budget: ₹8,000 - ₹12,000
Location: Rohini

Lifestyle:
Food: Vegetarian
Smoking: No
Cleanliness: High
Sleep Time: 11 PM
Wake Time: 7 AM
Occupation: Student
```

---

## 4. Technology Stack

### Backend

- Python
- Flask
- Flask-JWT-Extended
- PyMongo / MongoEngine
- REST API

### Database

- MongoDB
- MongoDB Sharding
- MongoDB Replica Sets

### AI/ML

- Python
- NumPy
- Pandas
- Scikit-learn
- Cosine Similarity
- Random Forest (future supervised-learning phase)

### Development and Testing

- Postman
- Git
- GitHub
- VS Code

### Frontend

The backend is designed to support:

- React.js
- HTML/CSS/JavaScript

---

## 5. Database Design

The main MongoDB collections are:

```text
users
rooms
partner_profiles
requests
matches
messages
ratings
```

### users

Stores authentication and basic user information.

```json
{
  "_id": "ObjectId",
  "name": "Rahul",
  "email": "rahul@example.com",
  "password": "hashed_password",
  "role": "room_owner",
  "location": {
    "city": "Delhi",
    "area": "Rohini"
  }
}
```

### rooms

Stores information about available rooms.

```json
{
  "_id": "ObjectId",
  "owner_id": "ObjectId",
  "location": {
    "city": "Delhi",
    "area": "Rohini"
  },
  "rent": 12000,
  "room_type": "2BHK",
  "available_from": "2026-10-01",
  "facilities": [
    "WiFi",
    "AC",
    "Parking"
  ],
  "preferred_gender": "Any",
  "status": "available"
}
```

### partner_profiles

Stores roommate preferences and lifestyle information.

```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "age": 23,
  "occupation": "Student",
  "preferred_location": "Rohini",
  "budget": {
    "min": 7000,
    "max": 13000
  },
  "lifestyle": {
    "food": "vegetarian",
    "smoking": false,
    "drinking": false,
    "cleanliness": 5,
    "sleep_time": "23:00",
    "wake_time": "07:00"
  }
}
```

### requests

Stores requests between Room Owners and Partner Seekers.

```json
{
  "_id": "ObjectId",
  "room_id": "ObjectId",
  "owner_id": "ObjectId",
  "seeker_id": "ObjectId",
  "status": "pending",
  "created_at": "2026-09-26T12:00:00Z"
}
```

### matches

Stores calculated compatibility results.

```json
{
  "_id": "ObjectId",
  "room_id": "ObjectId",
  "seeker_id": "ObjectId",
  "compatibility_score": 93,
  "created_at": "2026-09-26T12:00:00Z"
}
```

---

## 6. AI/ML Compatibility Matching

The application will calculate compatibility instead of relying only on simple database filters.

Possible features include:

- Location compatibility
- Budget compatibility
- Food preference
- Smoking preference
- Drinking preference
- Cleanliness
- Sleep schedule
- Wake-up schedule
- Occupation
- Room type
- Facilities
- Gender preference
- Lifestyle preferences

Example:

```text
Location compatibility     = 100%
Budget compatibility       = 90%
Food compatibility         = 100%
Smoking compatibility      = 100%
Sleep compatibility        = 80%
Cleanliness compatibility  = 90%
```

A weighted compatibility score can then be calculated.

Example:

```text
Final Score =
    Location      × 20%
  + Budget        × 25%
  + Lifestyle     × 30%
  + Preferences   × 25%
```

The final API can return:

```json
{
  "partner_id": "P101",
  "name": "Aman",
  "compatibility": 93
}
```

### ML Development Strategy

#### Phase 1: Content-Based Matching

Use:

- Feature encoding
- Normalization
- Weighted similarity
- Cosine similarity

This allows the system to work even when there is little historical user data.

#### Phase 2: Supervised Machine Learning

After enough interaction data is collected, training data can contain:

```text
location_match
budget_difference
food_match
smoking_match
sleep_difference
cleanliness_difference
occupation_match
request_sent
request_accepted
```

Possible models:

- Logistic Regression
- Random Forest
- XGBoost

The model can learn from historical accepted/rejected requests and improve recommendations.

---

## 7. Distributed Database Design

A major objective of this project is to demonstrate distributed database concepts using MongoDB.

### 7.1 Horizontal Fragmentation / Sharding

Data can be distributed according to geographical location.

```text
Delhi Users/Rooms
        |
        v
     Shard 1

Noida Users/Rooms
        |
        v
     Shard 2

Gurgaon Users/Rooms
        |
        v
     Shard 3
```

For example:

```text
Delhi    -> Shard 1
Noida    -> Shard 2
Gurgaon  -> Shard 3
```

This is useful because room searches are strongly location-oriented.

### 7.2 Replication

MongoDB replica sets can provide redundancy.

```text
             PRIMARY
                |
       +--------+--------+
       |                 |
       v                 v
 SECONDARY 1         SECONDARY 2
```

If the primary node fails, another replica can become primary.

Benefits:

- High availability
- Fault tolerance
- Data redundancy
- Improved reliability

### 7.3 Data Transparency

Although the database may contain multiple shards/nodes, the user sees a single application.

For example:

```http
GET /api/search/rooms?city=Delhi
```

The user does not need to know which database node stores the data.

### 7.4 Distributed Query

A search can involve data stored across multiple shards.

The application/database layer can retrieve relevant records and combine the results before returning them to the client.

---

## 8. REST API Design

### Authentication

```http
POST /api/auth/register
POST /api/auth/login
```

### Rooms

```http
POST   /api/rooms
GET    /api/rooms
GET    /api/rooms/<id>
PUT    /api/rooms/<id>
DELETE /api/rooms/<id>
```

### Partner Profiles

```http
POST /api/partners/profile
GET  /api/partners/profile
PUT  /api/partners/profile
```

### Search

```http
GET /api/search/rooms
GET /api/search/partners
```

### Matching

```http
GET /api/matching/partners/<room_id>
GET /api/matching/rooms/<partner_id>
```

### Requests

```http
POST /api/rooms/<room_id>/request
GET  /api/requests/my-requests
PUT  /api/requests/<request_id>/accept
PUT  /api/requests/<request_id>/reject
```

---

## 9. Recommended Project Structure

```text
room-partner-finder/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── config/
│   └── database.py
│
├── models/
│   ├── user.py
│   ├── room.py
│   ├── partner.py
│   ├── request.py
│   └── match.py
│
├── routes/
│   ├── auth.py
│   ├── rooms.py
│   ├── partners.py
│   ├── requests.py
│   └── matching.py
│
├── ml/
│   ├── preprocessing.py
│   ├── compatibility.py
│   ├── train.py
│   └── model.pkl
│
├── utils/
│   ├── auth.py
│   └── helpers.py
│
└── tests/
    ├── test_auth.py
    ├── test_rooms.py
    └── test_matching.py
```

---

## 10. Authentication

JWT-based authentication can be used.

```text
Register
   |
   v
Password hashing
   |
   v
MongoDB
   |
   v
Login
   |
   v
JWT Token
   |
   v
Protected APIs
```

Passwords should never be stored as plain text.

Recommended:

```text
bcrypt
```

---

## 11. Complete Application Flow

```text
                    REGISTER
                       |
                       v
                Select User Type
                  /                            /                             v               v
         ROOM OWNER       PARTNER SEEKER
              |                 |
              v                 v
          Add Room         Add Profile
              |                 |
              +--------+--------+
                       |
                       v
                 MongoDB Cluster
                       |
                       v
                Distributed Search
                       |
                       v
                Feature Extraction
                       |
                       v
                  ML Matching
                       |
                       v
              Compatibility Score
                       |
                       v
              Recommended Matches
                       |
                       v
                Send Request
                       |
                       v
                 Accept/Reject
                       |
                       v
                     MATCH
```

---

## 12. Example Compatibility Output

```json
{
  "room": {
    "id": "R101",
    "location": "Rohini",
    "rent": 12000
  },
  "recommended_partners": [
    {
      "partner_id": "P101",
      "name": "Aman",
      "compatibility_score": 93
    },
    {
      "partner_id": "P205",
      "name": "Rohit",
      "compatibility_score": 87
    },
    {
      "partner_id": "P309",
      "name": "Karan",
      "compatibility_score": 81
    }
  ]
}
```

The displayed score is generated by the matching system from profile features; it should not be hard-coded.

---

## 13. Security Considerations

The backend should implement:

- Password hashing
- JWT authentication
- Protected routes
- Input validation
- Role-based authorization
- MongoDB query validation
- Environment variables for secrets
- CORS configuration
- Secure error handling

Example `.env`:

```env
MONGO_URI=mongodb://localhost:27017/room_partner_finder
JWT_SECRET=your_secret_key
FLASK_ENV=development
```

Do not commit `.env` to GitHub.

---

## 14. Installation

### Clone the repository

```bash
git clone <repository-url>
cd room-partner-finder
```

### Create virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start Flask

```bash
python app.py
```

The backend can run on:

```text
http://localhost:5000
```

---

## 15. Suggested requirements.txt

```text
Flask
Flask-CORS
Flask-JWT-Extended
pymongo
python-dotenv
bcrypt
numpy
pandas
scikit-learn
joblib
```

---

## 16. Testing with Postman

The complete API can be tested using Postman.

Recommended testing order:

```text
1. Register Room Owner
2. Login Room Owner
3. Create Room
4. Register Partner Seeker
5. Login Partner Seeker
6. Create Partner Profile
7. Search Rooms
8. Calculate Compatibility
9. Send Request
10. Login as Room Owner
11. View Requests
12. Accept/Reject Request
```

---

## 17. Distributed Database Concepts Demonstrated

This project can be used to demonstrate the following DDBMS concepts during a presentation or viva:

| Concept | Project Implementation |
|---|---|
| NoSQL Database | MongoDB |
| Distributed Database | MongoDB Cluster |
| Horizontal Fragmentation | Location-based data distribution |
| Sharding | Delhi/Noida/Gurgaon shards |
| Replication | MongoDB Replica Sets |
| Data Transparency | Single API over distributed data |
| Distributed Query | Search across distributed data |
| Fault Tolerance | Replica nodes |
| Scalability | Add additional shards |
| Indexing | Location, rent and preference indexes |
| Eventual Consistency | Suitable non-critical profile/search operations |

---

## 18. Future Enhancements

Possible future improvements:

- Real-time chat using WebSockets.
- Google Maps/location integration.
- Geospatial MongoDB queries.
- Email notifications.
- Push notifications.
- Advanced recommendation model.
- User ratings and reviews.
- Room image upload.
- Fraud/spam detection.
- Recommendation explanation such as:
  - "Both are non-smokers"
  - "Budget is closely matched"
  - "Same preferred location"
  - "Similar sleep schedule"

---

## 19. Project Learning Outcomes

After completing this project, the team will gain practical experience in:

- Flask backend development
- REST API development
- JWT authentication
- MongoDB and NoSQL data modeling
- Distributed database architecture
- MongoDB sharding
- Database replication
- Distributed query processing
- Machine learning integration
- Recommendation systems
- Feature engineering
- API testing
- Backend security
- Full-stack system architecture

---

## 20. Final Technology Architecture

```text
             React / HTML / JS
                     |
                     v
              Python Flask
                     |
       +-------------+-------------+
       |             |             |
       v             v             v
   Auth APIs      Room APIs    Matching APIs
       |             |             |
       +-------------+-------------+
                     |
                     v
              MongoDB Cluster
                     |
          +----------+----------+
          |          |          |
          v          v          v
       Delhi       Noida     Gurgaon
       Shard       Shard       Shard
          |          |          |
          +----------+----------+
                     |
                     v
                AI/ML Engine
                     |
                     v
          Compatibility Score
                     |
                     v
             Recommendations
```

---

## License

This project is intended for academic and educational purposes.
