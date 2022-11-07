GAMES=100000
URL="https://database.lichess.org/standard/lichess_db_standard_rated_2022-09.pgn.bz2"

mkdir -p data
curl $URL | bzip2 -d | python process_data.py
