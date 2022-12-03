GAMES=100000
URL="https://database.lichess.org/standard/lichess_db_standard_rated_2022-09.pgn.zst"

mkdir -p data
curl $URL | zstdcat | python process_data.py
