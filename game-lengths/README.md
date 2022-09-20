# Distrubtion of game length by chess variant
## Summary
Here, I present the distribution of the length of chess games by chess variant.

Standard chess games and Chess960 games typically terminate before the end of the 32nd move (64th ply). Atomic games are the shortest, often finishing before the end of the 11th move (22nd ply). While Horde games last the longest, generally terminating before the end of the 48th move (96th ply). 

I used the length of games played on [Lichess](https://lichess.org/) in August 2022. I sampled games from all available variants up to a limit of 100,000 games for each variant using the data provided by the [Lichess Open Database](https://database.lichess.org).
### Table

| Variant | Median game length | Modal game length |
| ------- | ------------------ | ----------------- |
| Standard | 32 | 31
| Antichess | 23 | 19
| Atomic | 11 | 4
| Chess960 | 32 | 30
| Crazyhouse | 26 | 25
| Horde | 48 | 49
| King of The Hill | 23 | 25
| Racing Kings | 14 | 15
| Three Check | 15 | 10

# Kernel density estimates
## All variants
![all variants](plots/all.svg)
## Standard
![standard](plots/standard.svg)
## Antichess
![antichess](plots/antichess.svg)
## Atomic
![atomic](plots/atomic.svg)
## Chess960
![standard](plots/chess960.svg)
## Crazyhouse
![standard](plots/crazyhouse.svg)
## Horde 
![standard](plots/horde.svg)
## King of The Hill 
![standard](plots/kingOfTheHill.svg)
## Racing Kings
![standard](plots/racingKings.svg)
## Three Check 
![standard](plots/threeCheck.svg)

## Notes
Games were taken from games played accross all time controls
