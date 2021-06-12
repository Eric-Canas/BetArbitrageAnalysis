# Bet Arbitrage Analysis
Crawler over oddschecker.com that looks for any inefficiency in the spanish betting market. If found, gets the best surebet for both, maximizing benefits and reducing the probability of being banned.


## Example of output
```
--------------------------------------------------
SURE BET FOUND! Sure win of 1.34%  
In futbol, on the match of Hoy at 18:00: BÃ©lgica vs Rusia.  
Best bets are: 2.10 (Luckya) - 3.50 (William-Hill) - 4.45 (Marathon-Bet).  
(BÃ©lgica - 2.10, Draw - 3.50,  Rusia - 4.45).  
You should bet 48.26% to BÃ©lgica, 28.959% to Draw, 22.777% to  Rusia.  
Best rounded bets: 15.0€ - 9.0€ - 7.0€. [Total bet: 31.0€].  
Profits range: 0.5€ (1.61%) - 0.5€ (1.61%) - 0.15€ (0.48%).  
Information extracted from https://www.oddschecker.com/es/futbol/internacional/euro-2020/belgica-rusia.  
--------------------------------------------------  
...  
--------------------------------------------------  
SURE BET FOUND! Sure win of 21.21%.  
In e-sports, on the match of dom. 13 jun. at 08:00: LGD Gaming vs Ultra Prime.  
Best bets are: 1.65 (Codere) - 5.50 (Luckya).  
(LGD Gaming - 1.65,  Ultra Prime - 5.50).  
You should bet 76.92% to LGD Gaming, 23.077% to  Ultra Prime.  
Best rounded bets: 10.0€ - 3.0€. [Total bet: 13.0€].  
Profits range: 3.5€ (26.92%) - 3.5€ (26.92%).  
Information extracted from https://www.oddschecker.com/es/e-sports/league-of-legends/lgd-gaming-ultra-prime.  
--------------------------------------------------  
...  
--------------------------------------------------  
Bets analyzed: 127  
Sure bets found: 13  
Bad bets found: 114  
Best value found 21.21%  
```
