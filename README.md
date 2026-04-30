# DigitalTwin-TulipTech
Digital Twin Interface for the course Multidisciplinary Project at TU Delft.  

**Group 16**: TU Delft - Núria Seguí Vidal · Gonçalo Fernández-Nespral Vaz · Twan Grooff · Javier Gil Avilés · Tom van Beekhoff 

## How to Run It
### Step 1 - Install dependencies:

```bash
cd digital_twin
pip install -r requirements.txt
```

### Step 2 - Start the server:

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3 - Seed the database with test data:
Open a second terminal and run:

```bash
curl -X POST http://localhost:8000/api/sensors/ \
  -H "Content-Type: application/json" \
  -d '{"stand_id": "A1", "temperature": 21.4, "humidity": 68.5}'
  ```


### Step 4 - Open the dashboard:
Navigate to http://localhost:8000 in your browser. You'll see the live preview above.


## Project Folder Structure
Structure followed for this project. 

```bash
digital_twin/
│
├── backend/                  
│   ├── main.py               
│   ├── database.py           
│   ├── models.py             
│   ├── schemas.py            
│   ├── crud.py               
│   └── routers/
│       └── sensors.py        
│
├── frontend/
│   └── index.html            
│
├── greenhouse.db             
└── requirements.txt         
```