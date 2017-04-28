

team_df <- data.frame(team_info = c('Arizona:D-backs:ARI',
                                    'Atlanta:Braves:ATL',
                                    'Baltimore:Orioles:BAL',
                                    'Boston:Red Sox:BOS',
                                    'Chicago:Cubs:CHC',
                                    'Chicago:White Sox:CHW',
                                    'Cincinnati:Reds:CIN',
                                    'Cleveland:Indians:CLE',
                                    'Colorado:Rockies:COL',
                                    'Detroit:Tigers:DET',
                                    'Florida:Marlins:FLA',
                                    'Houston:Astros:HOU',
                                    'Kansas City:Royals:KAN',
                                    'Los Angeles:Angels:LAA',
                                    'Los Angeles:Dodgers:LAD',
                                    'Milwaukee:Brewers:MIL',
                                    'Minnesota:Twins:MIN',
                                    'New York:Mets:NYM',
                                    'New York:Yankees:NYY',
                                    'Oakland:Athletics:OAK',
                                    'Philadelphia:Phillies:PHI',
                                    'Pittsburgh:Pirates:PIT',
                                    'San Diego:Padres:SD',
                                    'San Francisco:Giants:SF',
                                    'Seattle:Mariners:SEA',
                                    'St. Louis:Cardinals:STL',
                                    'Tampa Bay:Rays:TB',
                                    'Texas:Rangers:TEX',
                                    'Toronto:Blue Jays:TOR',
                                    'Washington:Nationals:WAS')) %>% 
                        separate(team_info, c('city', 'team_name', 'team_abbr'), sep = ':') %>% 
                        mutate_each(funs(tolower)) %>%
                        mutate(team_id = 1:30) %>% 
                        select(team_id, team_name, city, team_abbr) -> out

write.csv(out, 'team_name_df.csv', row.names = F)
