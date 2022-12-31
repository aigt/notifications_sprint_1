#!/bin/bash
echo "sleeping for 10 seconds"
sleep 10

echo mongo_setup.sh time now: `date +"%T" `
mongosh --host mongo1:27017 <<EOF
  var cfg = {
    "_id": "rs0",
    "version": 1,
    "members": [
      {
        "_id": 0,
        "host": "localhost:27017",
        "priority": 2
      }
    ]
  };
  rs.initiate(cfg);

use ugc_movies
var moviesReviewCollName = "movies_review"
var bookmarkCollName = "bookmark"
var moviesRatingCollName = "movies_rating"


db.createCollection(moviesReviewCollName)
var moviesReviewColl = db.getCollection(moviesReviewCollName)
moviesReviewColl.createIndex({ "movie_id": 1 }, { "unique": true })


db.createCollection(bookmarkCollName)
var bookmarkColl = db.getCollection(bookmarkCollName)
bookmarkColl.createIndex({ "user_id": 1 }, { "unique": true })


db.createCollection(moviesRatingCollName)
var moviesRatingColl = db.getCollection(moviesRatingCollName)
moviesRatingColl.createIndex({ "movie_id": 1 }, { "unique": true })
EOF
