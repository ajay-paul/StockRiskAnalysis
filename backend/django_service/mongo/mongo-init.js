db = connect("mongodb://localhost:27017/admin");

db.createUser({
    user: "mongo_user",
    pwd: "mongo_password",
    roles: [
        { role: "readWrite", db: "stock_data" }
    ]
});

db = connect("mongodb://localhost:27017/stock_data");

db.createCollection("stocks");
db.createCollection("predictions");

print("Initialized MongoDB with 'stock_data' database and collections.");
