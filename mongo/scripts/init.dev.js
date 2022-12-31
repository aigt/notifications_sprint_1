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
