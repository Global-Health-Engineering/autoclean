# AutoClean Report

**Dataset:** Manager Data
**Generated:** 2026-01-06 17:08:40

---

## Summary

- **Original shape:** 28187 rows × 18 columns
- **After preprocessing:** 28187 rows × 18 columns
- **Total structural errors fixed:** 3219

---

## Preprocessing

- **Columns renamed:** 18

| Original | New |
|----------|-----|
| Timestamp | timestamp |
| How old are you? | how_old_are_you_ |
| What industry do you work in? | what_industry_do_you_work_in_ |
| Job title | job_title |
| If your job title needs additional context, please clarify here: | if_your_job_title_needs_additional_context_please_clarify_here_ |
| What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.) | what_is_your_annual_salary_youll_indicate_the_currency_in_a_later_question_if_you_are_part_time_or_hourly_please_enter_an_annualized_equivalent_what_you_would_earn_if_you_worked_the_job_40_hours_a_week_52_weeks_a_year_ |
| How much additional monetary compensation do you get, if any (for example, bonuses or overtime in an average year)? Please only include monetary compensation here, not the value of benefits. | how_much_additional_monetary_compensation_do_you_get_if_any_for_example_bonuses_or_overtime_in_an_average_year_please_only_include_monetary_compensation_here_not_the_value_of_benefits_ |
| Please indicate the currency | please_indicate_the_currency |
| If "Other," please indicate the currency here:  | if_"other_"_please_indicate_the_currency_here_ |
| If your income needs additional context, please provide it here: | if_your_income_needs_additional_context_please_provide_it_here_ |
| ... | (8 more) |

---

## Duplicates

No duplicates found.

---

## Structural Errors

- **Columns processed:** 1
- **Total values changed:** 3219

### what_country_do_you_work_in_

- **Similarity method:** embeddings
- **Clustering method:** hierarchical
- **Canonical selection:** most_frequent
- **Threshold:** 0.8
- **Embedding model:** text-embedding-3-small
- **Unique values before:** 328
- **Unique values after:** 241
- **Values changed:** 3219

#### Clustering Results

| Original Values | Canonical |
|-----------------|-----------|
| US, USA | USA |
| United States, United states, united states, The United States, UNITED STATES, united States, Uniited States, UNited States, United  States | United States |
| Canada | Canada |
| U.S., u.s., U.S, U. S., U.s., U. S | U.S. |
| United Kingdom, United Kingdom., United kingdom, united kingdom | United Kingdom |
| UK | UK |
| United States of America, united states of america, United State of America, United States of American, United Sates of America, United States of america, United states of America, United States Of America, United states of america | United States of America |
| Usa, U.SA, uSA, UsA | Usa |
| Australia, Australian | Australia |
| Germany | Germany |
| usa | usa |
| England | England |
| Ireland, ireland | Ireland |
| New Zealand, New zealand, new zealand | New Zealand |
| Us | Us |
| Uk | Uk |
| The Netherlands, Netherlands, netherlands, the Netherlands, The netherlands, the netherlands | Netherlands |
| France | France |
| U.S.A, U.S.A., U.s.a. | U.S.A. |
| Spain | Spain |
| Scotland | Scotland |
| United State, United Stated, United Statws, United Sates, United Stattes, United Statea, United Statees, United Sttes, United Stateds, United STates, United Statss | United State |
| Sweden | Sweden |
| us | us |
| Switzerland, SWITZERLAND, switzerland | Switzerland |
| Belgium | Belgium |
| canada, CANADA, Canad, Canadá | canada |
| Japan | Japan |
| Denmark, Danmark, denmark | Denmark |
| India | India |
| America | America |
| Unites States, Uniteed States, Unites states, Unite States, Unitied States | Unites States |
| South Africa, South africa | South Africa |
| Singapore | Singapore |
| Austria | Austria |
| finland, Finland | Finland |
| Norway | Norway |
| Israel | Israel |
| Italy | Italy |
| Malaysia | Malaysia |
| U.K., U.K | U.K. |
| Brazil | Brazil |
| Philippines, philippines | Philippines |
| Poland | Poland |
| England/UK, England, UK., England, UK, England, United Kingdom | England, UK |
| China | China |
| Colombia | Colombia |
| Mexico | Mexico |
| Thailand | Thailand |
| Wales (United Kingdom), Wales, Wales, UK, Wales (UK) | Wales |
| Czech republic, Czechia, czech republic, Czech Republic | Czech Republic |
| NZ | NZ |
| Nigeria, NIGERIA | Nigeria |
| Argentina | Argentina |
| Great Britain | Great Britain |
| Hong Kong, Hong KongKong | Hong Kong |
| Greece | Greece |
| germany | germany |
| Romania | Romania |
| uk | uk |
| Taiwan | Taiwan |
| South Korea | South Korea |
| Portugal | Portugal |
| Northern Ireland, Northern Ireland, United Kingdom | Northern Ireland |
| United Kingdom (England), UK (England) | United Kingdom (England) |
| Latvia | Latvia |
| Puerto Rico | Puerto Rico |
| United Stares | United Stares |
| australia, Australi | australia |
| UnitedStates | UnitedStates |
| england, ENGLAND | england |
| Pakistan | Pakistan |
| 🇺🇸 | 🇺🇸 |
| ISA | ISA |
| Luxembourg, Luxemburg | Luxembourg |
| spain | spain |
| Chile | Chile |
| Scotland, UK | Scotland, UK |
| Saudi Arabia | Saudi Arabia |
| Ghana | Ghana |
| Kenya | Kenya |
| INDIA, india | india |
| Bermuda | Bermuda |
| Sri lanka, Sri Lanka | Sri lanka |
| FRANCE, france | FRANCE |
| Hungary | Hungary |
| Unted States, Untied States | Unted States |
| United Arab Emirates, UAE | United Arab Emirates |
| Bangladesh | Bangladesh |
| United Status | United Status |
| Turkey | Turkey |
| Canda | Canda |
| New Zealand Aotearoa, Aotearoa New Zealand | New Zealand Aotearoa |
| I.S. | I.S. |
| The US | The US |
| Vietnam | Vietnam |
| Remote | Remote |
| Lithuania | Lithuania |
| Indonesia | Indonesia |
| Slovenia | Slovenia |
| USA tomorrow | USA tomorrow |
| Bulgaria | Bulgaria |
| Estonia | Estonia |
| Morocco | Morocco |
| Zimbabwe | Zimbabwe |
| Croatia, croatia | Croatia |
| Cyprus | Cyprus |
| U.S> | U.S> |
| Kuwait | Kuwait |
| Contracts | Contracts |
| USA-- Virgin Islands | USA-- Virgin Islands |
| We don't get raises, we get quarterly bonuses, but they periodically asses income in the area you work, so I got a raise because a 3rd party assessment showed I was paid too little for the area we were located | We don't get raises, we get quarterly bonuses, but they periodically asses income in the area you work, so I got a raise because a 3rd party assessment showed I was paid too little for the area we were located |
| Britain | Britain |
| Canada, Ottawa, ontario | Canada, Ottawa, ontario |
| Global | Global |
| Worldwide (based in US but short term trips aroudn the world) | Worldwide (based in US but short term trips aroudn the world) |
| Canadw | Canadw |
| United States (I work from home and my clients are all over the US/Canada/PR | United States (I work from home and my clients are all over the US/Canada/PR |
| United Statesp | United Statesp |
| Trinidad and Tobago | Trinidad and Tobago |
| Cayman Islands | Cayman Islands |
| Can | Can |
| I am located in Canada but I work for a company in the US | I am located in Canada but I work for a company in the US |
| Uniyed states | Uniyed states |
| Uniyes States | Uniyes States |
| United States of Americas | United States of Americas |
| U.A. | U.A. |
| US of A | US of A |
| Rwanda | Rwanda |
| United Kindom | United Kindom |
| Currently finance | Currently finance |
| Serbia | Serbia |
| Russia | Russia |
| UXZ | UXZ |
| Canada and USA | Canada and USA |
| Catalonia | Catalonia |
| $2,175.84/year is deducted for benefits | $2,175.84/year is deducted for benefits |
| Italy (South) | Italy (South) |
| Jersey, Channel islands | Jersey, Channel islands |
| Virginia | Virginia |
| Afghanistan | Afghanistan |
| USS | USS |
| Hartford | Hartford |
| Japan, US Gov position | Japan, US Gov position |
| Csnada | Csnada |
| Mainland China | Mainland China |
| UK (Northern Ireland) | UK (Northern Ireland) |
| UK for U.S. company | UK for U.S. company |
| Cambodia | Cambodia |
| Eritrea | Eritrea |
| For the United States government, but posted overseas | For the United States government, but posted overseas |
| IS | IS |
| United Kingdomk | United Kingdomk |
| Cuba | Cuba |
| Cote d'Ivoire | Cote d'Ivoire |
| From Romania, but for an US based company | From Romania, but for an US based company |
| Somalia | Somalia |
| England, Gb | England, Gb |
| U.K. (northern England) | U.K. (northern England) |
| NL | NL |
| Nederland | Nederland |
| Slovakia | Slovakia |
| Sierra Leone | Sierra Leone |
| Englang | Englang |
| United statew | United statew |
| bonus based on meeting yearly goals set w/ my supervisor | bonus based on meeting yearly goals set w/ my supervisor |
| International | International |
| The Bahamas | The Bahamas |
| I earn commission on sales. If I meet quota, I'm guaranteed another 16k min. Last year i earned an additional 27k. It's not uncommon for people in my space to earn 100k+ after commission. | I earn commission on sales. If I meet quota, I'm guaranteed another 16k min. Last year i earned an additional 27k. It's not uncommon for people in my space to earn 100k+ after commission. |
| Costa Rica | Costa Rica |
| United Statues | United Statues |
| USA (company is based in a US territory, I work remote) | USA (company is based in a US territory, I work remote) |
| UK, remote | UK, remote |
| USAB | USAB |
| Qatar | Qatar |
| Remote (philippines) | Remote (philippines) |
| Unites kingdom | Unites kingdom |
| united stated | united stated |
| Panamá | Panamá |
| Austria, but I work remotely for a Dutch/British company | Austria, but I work remotely for a Dutch/British company |
| I work for an US based company but I'm from Argentina. | I work for an US based company but I'm from Argentina. |
| I was brought in on this salary to help with the EHR and very quickly was promoted to current position but compensation was not altered. | I was brought in on this salary to help with the EHR and very quickly was promoted to current position but compensation was not altered. |
| Uniter Statez | Uniter Statez |
| Congo | Congo |
| Uruguay | Uruguay |
| Brasil | Brasil |
| n/a (remote from wherever I want) | n/a (remote from wherever I want) |
| singapore | singapore |
| US govt employee overseas, country withheld | US govt employee overseas, country withheld |
| Uganda | Uganda |
| Malta | Malta |
| Africa | Africa |
| Ecuador | Ecuador |
| San Francisco | San Francisco |
| Usat | Usat |
| Unitef Stated | Unitef Stated |
| UA | UA |
| USaa | USaa |
| Ukraine | Ukraine |
| america | america |
| United States- Puerto Rico | United States- Puerto Rico |
| From New Zealand but on projects across APAC | From New Zealand but on projects across APAC |
| Y | Y |
| United y | United y |
| Isle of Man | Isle of Man |
| europe | europe |
| California | California |
| UK, but for globally fully remote company | UK, but for globally fully remote company |
| México | México |
| Jamaica | Jamaica |
| uS | uS |
| USD | USD |
| USA, but for foreign gov't | USA, but for foreign gov't |
| japan | japan |
| Jordan | Jordan |
| ARGENTINA BUT MY ORG IS IN THAILAND | ARGENTINA BUT MY ORG IS IN THAILAND |
| I work for a UAE-based organization, though I am personally in the US. | I work for a UAE-based organization, though I am personally in the US. |
| na | na |
| Policy | Policy |
| hong konh | hong konh |
| United States is America | United States is America |
| Liechtenstein | Liechtenstein |
| Company in Germany. I work from Pakistan. | Company in Germany. I work from Pakistan. |
| Bosnia and Herzegovina | Bosnia and Herzegovina |
| pakistan | pakistan |
| London | London |
| ss | ss |
| dbfemf | dbfemf |
| ibdia | ibdia |
| LOUTRELAND | LOUTRELAND |
| ff | ff |
| Myanmar | Myanmar |
| Burma | Burma |
| Tanzania | Tanzania |
| Česká republika | Česká republika |
| Italia | Italia |
| Egypt | Egypt |
| Liberia | Liberia |
| 1 | 1 |
| Nigeria + UK | Nigeria + UK |
| Zambia | Zambia |

#### Value Counts (Original Data)

| Value | Count |
|-------|-------|
| United States | 9697 |
| USA | 8425 |
| US | 2637 |
| Canada | 1649 |
| United Kingdom | 613 |
| U.S. | 603 |
| UK | 597 |
| United States of America | 474 |
| Usa | 466 |
| Australia | 387 |
| United states | 221 |
| Germany | 193 |
| usa | 188 |
| England | 166 |
| Ireland | 122 |
| united states | 119 |
| New Zealand | 117 |
| Us | 111 |
| Uk | 91 |
| France | 67 |
| Netherlands | 54 |
| Spain | 47 |
| U.S.A. | 47 |
| Scotland | 46 |
| Sweden | 41 |
| us | 38 |
| Switzerland | 36 |
| Belgium | 35 |
| The Netherlands | 28 |
| Japan | 28 |
| canada | 27 |
| India | 22 |
| U.S | 22 |
| America | 22 |
| United State | 20 |
| Singapore | 19 |
| Denmark | 19 |
| Austria | 18 |
| South Africa | 17 |
| United kingdom | 16 |
| Finland | 15 |
| Israel | 14 |
| Italy | 14 |
| Norway | 14 |
| Unites States | 14 |
| Malaysia | 13 |
| U.K. | 12 |
| Brazil | 11 |
| U.S.A | 10 |
| Philippines | 10 |
| Poland | 10 |
| United Stated | 9 |
| China | 9 |
| Colombia | 8 |
| Thailand | 7 |
| U. S. | 7 |
| United States of america | 7 |
| UNITED STATES | 7 |
| Mexico | 7 |
| The United States | 7 |
| NZ | 6 |
| United Sates | 6 |
| united kingdom | 5 |
| uk | 5 |
| South Korea | 5 |
| germany | 5 |
| CANADA | 5 |
| Nigeria | 5 |
| Portugal | 5 |
| Greece | 5 |
| Taiwan | 5 |
| Argentina | 5 |
| Great Britain | 5 |
| United states of America | 5 |
| Romania | 5 |
| 🇺🇸 | 4 |
| England, UK | 4 |
| Latvia | 4 |
| Wales | 4 |
| Puerto Rico | 4 |
| UnitedStates | 4 |
| Pakistan | 4 |
| denmark | 4 |
| United Stares | 4 |
| United State of America | 4 |
| united States | 4 |
| Hong Kong | 4 |
| New zealand | 4 |
| United States Of America | 4 |
| ireland | 3 |
| Saudi Arabia | 3 |
| spain | 3 |
| Northern Ireland | 3 |
| Kenya | 3 |
| Czech Republic | 3 |
| australia | 3 |
| ISA | 3 |
| England, United Kingdom | 3 |
| Unites states | 3 |
| Ghana | 3 |
| Chile | 3 |
| netherlands | 3 |
| U.s. | 3 |
| Scotland, UK | 3 |
| United Statea | 3 |
| Indonesia | 2 |
| Slovenia | 2 |
| Vietnam | 2 |
| United Status | 2 |
| Lithuania | 2 |
| I.S. | 2 |
| United STates | 2 |
| The US | 2 |
| Unite States | 2 |
| england | 2 |
| Turkey | 2 |
| Canda | 2 |
| The netherlands | 2 |
| Bulgaria | 2 |
| Remote | 2 |
| South africa | 2 |
| Luxembourg | 2 |
| United Sates of America | 2 |
| UK (England) | 2 |
| Zimbabwe | 2 |
| USA tomorrow | 2 |
| United States of American | 2 |
| india | 2 |
| Hungary | 2 |
| ENGLAND | 2 |
| Estonia | 2 |
| Cyprus | 2 |
| Morocco | 2 |
| new zealand | 2 |
| u.s. | 2 |
| Bermuda | 2 |
| Bangladesh | 2 |
| United Kingdom (England) | 2 |
| Austria, but I work remotely for a Dutch/British company | 1 |
| I work for an US based company but I'm from Argentina. | 1 |
| I was brought in on this salary to help with the EHR and very quickly was promoted to current position but compensation was not altered. | 1 |
| Uniter Statez | 1 |
| U. S | 1 |
| Congo | 1 |
| Uruguay | 1 |
| SWITZERLAND | 1 |
| San Francisco | 1 |
| uSA | 1 |
| Luxemburg | 1 |
| Usat | 1 |
| Ecuador | 1 |
| Africa | 1 |
| Malta | 1 |
| Uganda | 1 |
| US govt employee overseas, country withheld | 1 |
| Unitef Stated | 1 |
| USaa | 1 |
| singapore | 1 |
| n/a (remote from wherever I want) | 1 |
| UA | 1 |
| United Stateds | 1 |
| Wales, UK | 1 |
| Croatia | 1 |
| Brasil | 1 |
| united states of america | 1 |
| Ukraine | 1 |
| ibdia | 1 |
| United States is America | 1 |
| Liechtenstein | 1 |
| Company in Germany. I work from Pakistan. | 1 |
| croatia | 1 |
| Canadá | 1 |
| INDIA | 1 |
| Bosnia and Herzegovina | 1 |
| NIGERIA | 1 |
| pakistan | 1 |
| London | 1 |
| ss | 1 |
| dbfemf | 1 |
| LOUTRELAND | 1 |
| Policy | 1 |
| philippines | 1 |
| ff | 1 |
| Myanmar | 1 |
| Burma | 1 |
| Tanzania | 1 |
| Česká republika | 1 |
| Italia | 1 |
| Hong KongKong | 1 |
| Egypt | 1 |
| Liberia | 1 |
| 1 | 1 |
| Nigeria + UK | 1 |
| hong konh | 1 |
| na | 1 |
| america | 1 |
| México | 1 |
| switzerland | 1 |
| United States- Puerto Rico | 1 |
| From New Zealand but on projects across APAC | 1 |
| Y | 1 |
| United y | 1 |
| Wales (UK) | 1 |
| Isle of Man | 1 |
| Northern Ireland, United Kingdom | 1 |
| europe | 1 |
| California | 1 |
| UK, but for globally fully remote company | 1 |
| Australian | 1 |
| Jamaica | 1 |
| Aotearoa New Zealand | 1 |
| uS | 1 |
| USD | 1 |
| USA, but for foreign gov't | 1 |
| japan | 1 |
| Jordan | 1 |
| United Statss | 1 |
| ARGENTINA BUT MY ORG IS IN THAILAND | 1 |
| United states of america | 1 |
| UsA | 1 |
| I work for a UAE-based organization, though I am personally in the US. | 1 |
| United  States | 1 |
| france | 1 |
| the netherlands | 1 |
| Wales (United Kingdom) | 1 |
| Panamá | 1 |
| U.SA | 1 |
| I am located in Canada but I work for a company in the US | 1 |
| Uniyed states | 1 |
| Uniyes States | 1 |
| United States of Americas | 1 |
| U.A. | 1 |
| Czech republic | 1 |
| Czechia | 1 |
| US of A | 1 |
| Rwanda | 1 |
| United Arab Emirates | 1 |
| United Kindom | 1 |
| UNited States | 1 |
| Currently finance | 1 |
| Serbia | 1 |
| Russia | 1 |
| UXZ | 1 |
| czech republic | 1 |
| Canada and USA | 1 |
| Catalonia | 1 |
| $2,175.84/year is deducted for benefits | 1 |
| Italy (South) | 1 |
| Jersey, Channel islands | 1 |
| Can | 1 |
| Cayman Islands | 1 |
| Afghanistan | 1 |
| Global | 1 |
| Kuwait | 1 |
| Sri lanka | 1 |
| Contracts | 1 |
| USA-- Virgin Islands | 1 |
| United Statws | 1 |
| England/UK | 1 |
| We don't get raises, we get quarterly bonuses, but they periodically asses income in the area you work, so I got a raise because a 3rd party assessment showed I was paid too little for the area we were located | 1 |
| England, UK. | 1 |
| Britain | 1 |
| Canada, Ottawa, ontario | 1 |
| FRANCE | 1 |
| United Statees | 1 |
| Uniited States | 1 |
| Worldwide (based in US but short term trips aroudn the world) | 1 |
| Canadw | 1 |
| United States (I work from home and my clients are all over the US/Canada/PR | 1 |
| Unted States | 1 |
| United Statesp | 1 |
| United Stattes | 1 |
| United Kingdom. | 1 |
| U.S> | 1 |
| Trinidad and Tobago | 1 |
| Virginia | 1 |
| U.s.a. | 1 |
| united stated | 1 |
| I earn commission on sales. If I meet quota, I'm guaranteed another 16k min. Last year i earned an additional 27k. It's not uncommon for people in my space to earn 100k+ after commission. | 1 |
| the Netherlands | 1 |
| Nederland | 1 |
| Slovakia | 1 |
| Sierra Leone | 1 |
| Englang | 1 |
| United statew | 1 |
| UAE | 1 |
| bonus based on meeting yearly goals set w/ my supervisor | 1 |
| International | 1 |
| The Bahamas | 1 |
| Costa Rica | 1 |
| U.K | 1 |
| United Statues | 1 |
| Untied States | 1 |
| USA (company is based in a US territory, I work remote) | 1 |
| UK, remote | 1 |
| USAB | 1 |
| Unitied States | 1 |
| Qatar | 1 |
| United Sttes | 1 |
| Remote (philippines) | 1 |
| Unites kingdom | 1 |
| NL | 1 |
| U.K. (northern England) | 1 |
| USS | 1 |
| finland | 1 |
| Uniteed States | 1 |
| New Zealand Aotearoa | 1 |
| Hartford | 1 |
| Japan, US Gov position | 1 |
| Csnada | 1 |
| Mainland China | 1 |
| UK (Northern Ireland) | 1 |
| UK for U.S. company | 1 |
| Canad | 1 |
| Cambodia | 1 |
| Eritrea | 1 |
| Danmark | 1 |
| For the United States government, but posted overseas | 1 |
| IS | 1 |
| United Kingdomk | 1 |
| Cuba | 1 |
| Australi | 1 |
| Cote d'Ivoire | 1 |
| From Romania, but for an US based company | 1 |
| Somalia | 1 |
| England, Gb | 1 |
| Sri Lanka | 1 |
| Zambia | 1 |

---

## Postprocessing

No postprocessing changes applied.
