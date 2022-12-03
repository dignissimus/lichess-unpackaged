YEAR=2022
MONTH="08"
VARIANTS=(standard antichess atomic chess960 crazyhouse horde kingOfTheHill racingKings threeCheck)

mkdir -p data
for variant in ${VARIANTS[@]}; do
    echo "Reading game lengths for variant \`$variant\`"
    curl -s "https://database.lichess.org/$variant/lichess_db_${variant}_rated_$YEAR-$MONTH.pgn.zst" | zstdcat | perl parse_lengths.pl > "data/$variant.target"
done
