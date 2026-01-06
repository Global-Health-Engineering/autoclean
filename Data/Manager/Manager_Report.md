# AutoClean Report

**Dataset:** Manager Data
**Generated:** 2026-01-06 22:53:50

---

## Summary

- **Original shape:** 28187 rows × 18 columns
- **After preprocessing:** 28187 rows × 18 columns
- **Total structural errors fixed:** 3086

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

- **Columns processed:** 3
- **Total values changed:** 3086

### what_country_do_you_work_in_

- **Similarity method:** rapidfuzz
- **Clustering method:** hierarchical
- **Canonical selection:** most_frequent
- **Threshold:** 0.82
- **Unique values before:** 328
- **Unique values after:** 245
- **Values changed:** 203

#### Clustering Results

| Original Values | Canonical |
|-----------------|-----------|
| United States; United State; United Stated; United Statws; Unites States; United Sates; Uniited States; Unted States; United Statesp; United Stattes; United Statea; United Statees; UNited States; Uniyes States; United Status; Uniteed States; United Stares; Unite States; United Statues; Untied States; Unitied States; United Sttes; United Stateds; United STates; United Statss; United  States | United States |
| USA; U.SA | USA |
| US | US |
| Canada; Canda | Canada |
| U.S.; U.S | U.S. |
| United Kingdom; United Kingdom.; United Kindom; United Kingdomk; united kingdom | United Kingdom |
| UK | UK |
| United States of America; United State of America; United States of American; United Sates of America; United States of Americas; United States Of America; United States is America | United States of America |
| Usa; Usat | Usa |
| Australia; australia; Australi; Australian | Australia |
| United states; Uniyed states; Unites states; UnitedStates; United statew | United states |
| Germany; germany | Germany |
| usa | usa |
| England; Englang | England |
| Ireland; ireland | Ireland |
| united states; united States; united stated | united states |
| New Zealand; New zealand; new zealand | New Zealand |
| Us | Us |
| Uk | Uk |
| France; france | France |
| U.S.A; U.S.A. | U.S.A. |
| Netherlands; netherlands | Netherlands |
| Spain | Spain |
| Scotland | Scotland |
| Sweden | Sweden |
| us | us |
| Switzerland; switzerland | Switzerland |
| Belgium | Belgium |
| The Netherlands; the Netherlands; the netherlands | The Netherlands |
| Japan | Japan |
| canada | canada |
| America; america | America |
| India | India |
| Denmark; Danmark | Denmark |
| Singapore; singapore | Singapore |
| Austria | Austria |
| South Africa | South Africa |
| United kingdom; Unites kingdom | United kingdom |
| finland; Finland | Finland |
| Norway | Norway |
| Israel | Israel |
| Italy | Italy |
| Malaysia | Malaysia |
| U.K.; U.K | U.K. |
| Brazil; Brasil | Brazil |
| Philippines; philippines | Philippines |
| Poland | Poland |
| China | China |
| Mexico; México | Mexico |
| England/UK; England, UK.; England, UK; UK (England) | England, UK |
| U. S.; U. S | U. S. |
| Colombia | Colombia |
| The United States | The United States |
| UNITED STATES | UNITED STATES |
| United States of america | United States of america |
| Thailand | Thailand |
| NZ | NZ |
| Argentina | Argentina |
| Great Britain | Great Britain |
| Greece | Greece |
| United Kingdom (England); England, United Kingdom | England, United Kingdom |
| CANADA | CANADA |
| Czech republic; czech republic; Czech Republic | Czech Republic |
| Romania | Romania |
| uk | uk |
| Taiwan | Taiwan |
| United states of America | United states of America |
| South Korea | South Korea |
| Portugal | Portugal |
| Nigeria | Nigeria |
| Pakistan; pakistan | Pakistan |
| Hong Kong | Hong Kong |
| Latvia | Latvia |
| Puerto Rico | Puerto Rico |
| Wales | Wales |
| denmark | denmark |
| 🇺🇸 | 🇺🇸 |
| ISA | ISA |
| Northern Ireland | Northern Ireland |
| Canadw; Canad; Canadá | Canadw |
| Luxembourg; Luxemburg | Luxembourg |
| U.s. | U.s. |
| spain | spain |
| Chile | Chile |
| Scotland, UK | Scotland, UK |
| Saudi Arabia | Saudi Arabia |
| Ghana | Ghana |
| Kenya | Kenya |
| Bermuda | Bermuda |
| u.s. | u.s. |
| Hungary | Hungary |
| Bangladesh | Bangladesh |
| Turkey | Turkey |
| New Zealand Aotearoa; Aotearoa New Zealand | New Zealand Aotearoa |
| I.S. | I.S. |
| The US | The US |
| Vietnam | Vietnam |
| Remote | Remote |
| Lithuania | Lithuania |
| Indonesia | Indonesia |
| Slovenia | Slovenia |
| South africa | South africa |
| england | england |
| Uniter Statez; Unitef Stated | Uniter Statez |
| USA tomorrow | USA tomorrow |
| Bulgaria | Bulgaria |
| Estonia | Estonia |
| Morocco | Morocco |
| Zimbabwe | Zimbabwe |
| Wales, UK; Wales (UK) | Wales, UK |
| Croatia; croatia | Croatia |
| The netherlands | The netherlands |
| Cyprus | Cyprus |
| ENGLAND | ENGLAND |
| india | india |
| U.S> | U.S> |
| united states of america | united states of america |
| Kuwait | Kuwait |
| Sri lanka | Sri lanka |
| Contracts | Contracts |
| USA-- Virgin Islands | USA-- Virgin Islands |
| We don't get raises, we get quarterly bonuses, but they periodically asses income in the area you work, so I got a raise because a 3rd party assessment showed I was paid too little for the area we were located | We don't get raises, we get quarterly bonuses, but they periodically asses income in the area you work, so I got a raise because a 3rd party assessment showed I was paid too little for the area we were located |
| Britain | Britain |
| Canada, Ottawa, ontario | Canada, Ottawa, ontario |
| Global | Global |
| FRANCE | FRANCE |
| Worldwide (based in US but short term trips aroudn the world) | Worldwide (based in US but short term trips aroudn the world) |
| United States (I work from home and my clients are all over the US/Canada/PR | United States (I work from home and my clients are all over the US/Canada/PR |
| Trinidad and Tobago | Trinidad and Tobago |
| Cayman Islands | Cayman Islands |
| Can | Can |
| I am located in Canada but I work for a company in the US | I am located in Canada but I work for a company in the US |
| U.A. | U.A. |
| Czechia | Czechia |
| US of A | US of A |
| Rwanda | Rwanda |
| United Arab Emirates | United Arab Emirates |
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
| U.s.a. | U.s.a. |
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
| Cuba | Cuba |
| Cote d'Ivoire | Cote d'Ivoire |
| From Romania, but for an US based company | From Romania, but for an US based company |
| Somalia | Somalia |
| Wales (United Kingdom) | Wales (United Kingdom) |
| England, Gb | England, Gb |
| Sri Lanka | Sri Lanka |
| U.K. (northern England) | U.K. (northern England) |
| NL | NL |
| Nederland | Nederland |
| Slovakia | Slovakia |
| Sierra Leone | Sierra Leone |
| UAE | UAE |
| bonus based on meeting yearly goals set w/ my supervisor | bonus based on meeting yearly goals set w/ my supervisor |
| International | International |
| The Bahamas | The Bahamas |
| I earn commission on sales. If I meet quota, I'm guaranteed another 16k min. Last year i earned an additional 27k. It's not uncommon for people in my space to earn 100k+ after commission. | I earn commission on sales. If I meet quota, I'm guaranteed another 16k min. Last year i earned an additional 27k. It's not uncommon for people in my space to earn 100k+ after commission. |
| Costa Rica | Costa Rica |
| USA (company is based in a US territory, I work remote) | USA (company is based in a US territory, I work remote) |
| UK, remote | UK, remote |
| USAB | USAB |
| Qatar | Qatar |
| Remote (philippines) | Remote (philippines) |
| Panamá | Panamá |
| SWITZERLAND | SWITZERLAND |
| Austria, but I work remotely for a Dutch/British company | Austria, but I work remotely for a Dutch/British company |
| I work for an US based company but I'm from Argentina. | I work for an US based company but I'm from Argentina. |
| I was brought in on this salary to help with the EHR and very quickly was promoted to current position but compensation was not altered. | I was brought in on this salary to help with the EHR and very quickly was promoted to current position but compensation was not altered. |
| Congo | Congo |
| Uruguay | Uruguay |
| n/a (remote from wherever I want) | n/a (remote from wherever I want) |
| US govt employee overseas, country withheld | US govt employee overseas, country withheld |
| Uganda | Uganda |
| Malta | Malta |
| Africa | Africa |
| Ecuador | Ecuador |
| San Francisco | San Francisco |
| UA | UA |
| USaa | USaa |
| uSA | uSA |
| Ukraine | Ukraine |
| United States- Puerto Rico | United States- Puerto Rico |
| From New Zealand but on projects across APAC | From New Zealand but on projects across APAC |
| Y | Y |
| United y | United y |
| Isle of Man | Isle of Man |
| Northern Ireland, United Kingdom | Northern Ireland, United Kingdom |
| europe | europe |
| California | California |
| UK, but for globally fully remote company | UK, but for globally fully remote company |
| Jamaica | Jamaica |
| uS | uS |
| USD | USD |
| USA, but for foreign gov't | USA, but for foreign gov't |
| japan | japan |
| Jordan | Jordan |
| ARGENTINA BUT MY ORG IS IN THAILAND | ARGENTINA BUT MY ORG IS IN THAILAND |
| United states of america | United states of america |
| UsA | UsA |
| I work for a UAE-based organization, though I am personally in the US. | I work for a UAE-based organization, though I am personally in the US. |
| na | na |
| Policy | Policy |
| hong konh | hong konh |
| Liechtenstein | Liechtenstein |
| Company in Germany. I work from Pakistan. | Company in Germany. I work from Pakistan. |
| INDIA | INDIA |
| Bosnia and Herzegovina | Bosnia and Herzegovina |
| NIGERIA | NIGERIA |
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
| Hong KongKong | Hong KongKong |
| Egypt | Egypt |
| Liberia | Liberia |
| 1 | 1 |
| Nigeria + UK | Nigeria + UK |
| Zambia | Zambia |

### what_country_do_you_work_in_

- **Similarity method:** embeddings
- **Clustering method:** hierarchical
- **Canonical selection:** most_frequent
- **Threshold:** 0.7
- **Embedding model:** text-embedding-3-large
- **Unique values before:** 245
- **Unique values after:** 188
- **Values changed:** 1459

#### Clustering Results

| Original Values | Canonical |
|-----------------|-----------|
| United States; United States of America; United states; united states; united states of america; The United States; UNITED STATES; United States of america; United states of America; United states of america | United States |
| USA; usa | USA |
| US; us; Us | US |
| Canada; canada; CANADA | Canada |
| United Kingdom; Uk; United kingdom; U.K. | United Kingdom |
| U.S.; U.S>; u.s.; U. S.; U.s. | U.S. |
| UK; uk | UK |
| Usa | Usa |
| Australia | Australia |
| Germany | Germany |
| England | England |
| Ireland | Ireland |
| New Zealand; New Zealand Aotearoa | New Zealand |
| The Netherlands; Netherlands; Nederland; The netherlands | Netherlands |
| France; FRANCE | France |
| U.S.A.; US of A; U.s.a. | U.S.A. |
| Spain; spain | Spain |
| Scotland; Scotland, UK | Scotland |
| Sweden | Sweden |
| Switzerland; SWITZERLAND | Switzerland |
| Belgium | Belgium |
| Japan | Japan |
| Denmark; denmark | Denmark |
| America | America |
| India | India |
| Singapore | Singapore |
| South Africa; South africa | South Africa |
| Austria | Austria |
| Finland | Finland |
| Norway | Norway |
| England, UK; England, United Kingdom; England, Gb | England, UK |
| Israel | Israel |
| Italy | Italy |
| Malaysia | Malaysia |
| Brazil | Brazil |
| Philippines | Philippines |
| Poland | Poland |
| China | China |
| Mexico | Mexico |
| Colombia | Colombia |
| Czech Republic; Czechia; Česká republika | Czech Republic |
| Thailand | Thailand |
| Wales (United Kingdom); Wales; Wales, UK | Wales |
| NZ | NZ |
| Nigeria; NIGERIA | Nigeria |
| Argentina | Argentina |
| Great Britain | Great Britain |
| Northern Ireland; UK (Northern Ireland); Northern Ireland, United Kingdom | Northern Ireland |
| Hong Kong; Hong KongKong | Hong Kong |
| Greece | Greece |
| Puerto Rico; United States- Puerto Rico | Puerto Rico |
| Romania | Romania |
| Taiwan | Taiwan |
| South Korea | South Korea |
| Portugal | Portugal |
| Pakistan | Pakistan |
| ISA; IS | ISA |
| Canadw; Csnada | Canadw |
| Latvia | Latvia |
| england; ENGLAND | england |
| 🇺🇸 | 🇺🇸 |
| Luxembourg | Luxembourg |
| Chile | Chile |
| Saudi Arabia | Saudi Arabia |
| Ghana | Ghana |
| USaa; uSA; UsA | USaa |
| Kenya | Kenya |
| INDIA; india | india |
| Bermuda | Bermuda |
| Sri lanka; Sri Lanka | Sri lanka |
| Hungary | Hungary |
| United States (I work from home and my clients are all over the US/Canada/PR; USA (company is based in a US territory, I work remote) | United States (I work from home and my clients are all over the US/Canada/PR |
| U.A.; UA | U.A. |
| United Arab Emirates; UAE | United Arab Emirates |
| Bangladesh | Bangladesh |
| Turkey | Turkey |
| I.S. | I.S. |
| The US | The US |
| Vietnam | Vietnam |
| Remote | Remote |
| Lithuania | Lithuania |
| Indonesia | Indonesia |
| Slovenia | Slovenia |
| UK, remote; UK, but for globally fully remote company | UK, remote |
| Uniter Statez | Uniter Statez |
| USA tomorrow | USA tomorrow |
| Bulgaria | Bulgaria |
| Estonia | Estonia |
| Morocco | Morocco |
| Zimbabwe | Zimbabwe |
| Croatia | Croatia |
| Cyprus | Cyprus |
| Myanmar; Burma | Myanmar |
| Kuwait | Kuwait |
| Contracts | Contracts |
| USA-- Virgin Islands | USA-- Virgin Islands |
| We don't get raises, we get quarterly bonuses, but they periodically asses income in the area you work, so I got a raise because a 3rd party assessment showed I was paid too little for the area we were located | We don't get raises, we get quarterly bonuses, but they periodically asses income in the area you work, so I got a raise because a 3rd party assessment showed I was paid too little for the area we were located |
| Britain | Britain |
| Canada, Ottawa, ontario | Canada, Ottawa, ontario |
| Global | Global |
| Worldwide (based in US but short term trips aroudn the world) | Worldwide (based in US but short term trips aroudn the world) |
| Trinidad and Tobago | Trinidad and Tobago |
| Cayman Islands | Cayman Islands |
| Can | Can |
| I am located in Canada but I work for a company in the US | I am located in Canada but I work for a company in the US |
| Rwanda | Rwanda |
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
| Mainland China | Mainland China |
| UK for U.S. company | UK for U.S. company |
| Cambodia | Cambodia |
| Eritrea | Eritrea |
| For the United States government, but posted overseas | For the United States government, but posted overseas |
| Cuba | Cuba |
| Cote d'Ivoire | Cote d'Ivoire |
| From Romania, but for an US based company | From Romania, but for an US based company |
| Somalia | Somalia |
| U.K. (northern England) | U.K. (northern England) |
| NL | NL |
| Slovakia | Slovakia |
| Sierra Leone | Sierra Leone |
| bonus based on meeting yearly goals set w/ my supervisor | bonus based on meeting yearly goals set w/ my supervisor |
| International | International |
| The Bahamas | The Bahamas |
| I earn commission on sales. If I meet quota, I'm guaranteed another 16k min. Last year i earned an additional 27k. It's not uncommon for people in my space to earn 100k+ after commission. | I earn commission on sales. If I meet quota, I'm guaranteed another 16k min. Last year i earned an additional 27k. It's not uncommon for people in my space to earn 100k+ after commission. |
| Costa Rica | Costa Rica |
| USAB | USAB |
| Qatar | Qatar |
| Remote (philippines) | Remote (philippines) |
| Panamá | Panamá |
| Austria, but I work remotely for a Dutch/British company | Austria, but I work remotely for a Dutch/British company |
| I work for an US based company but I'm from Argentina. | I work for an US based company but I'm from Argentina. |
| I was brought in on this salary to help with the EHR and very quickly was promoted to current position but compensation was not altered. | I was brought in on this salary to help with the EHR and very quickly was promoted to current position but compensation was not altered. |
| Congo | Congo |
| Uruguay | Uruguay |
| n/a (remote from wherever I want) | n/a (remote from wherever I want) |
| US govt employee overseas, country withheld | US govt employee overseas, country withheld |
| Uganda | Uganda |
| Malta | Malta |
| Africa | Africa |
| Ecuador | Ecuador |
| San Francisco | San Francisco |
| Ukraine | Ukraine |
| From New Zealand but on projects across APAC | From New Zealand but on projects across APAC |
| Y | Y |
| United y | United y |
| Isle of Man | Isle of Man |
| europe | europe |
| California | California |
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
| Liechtenstein | Liechtenstein |
| Company in Germany. I work from Pakistan. | Company in Germany. I work from Pakistan. |
| Bosnia and Herzegovina | Bosnia and Herzegovina |
| London | London |
| ss | ss |
| dbfemf | dbfemf |
| ibdia | ibdia |
| LOUTRELAND | LOUTRELAND |
| ff | ff |
| Tanzania | Tanzania |
| Italia | Italia |
| Egypt | Egypt |
| Liberia | Liberia |
| 1 | 1 |
| Nigeria + UK | Nigeria + UK |
| Zambia | Zambia |

### what_country_do_you_work_in_

- **Similarity method:** embeddings
- **Clustering method:** hierarchical
- **Canonical selection:** most_frequent
- **Threshold:** 0.62
- **Embedding model:** text-embedding-3-large
- **Unique values before:** 188
- **Unique values after:** 163
- **Values changed:** 1424

#### Clustering Results

| Original Values | Canonical |
|-----------------|-----------|
| United States; U.S.; U.S.A.; The US | United States |
| USA; USA tomorrow | USA |
| US | US |
| Canada; Canadw; Canada and USA | Canada |
| United Kingdom; UK; Britain | United Kingdom |
| Usa; USaa | Usa |
| Australia | Australia |
| France; Germany | Germany |
| England; England, UK; england | England |
| New Zealand; NZ | New Zealand |
| Ireland; Northern Ireland | Ireland |
| Netherlands | Netherlands |
| Spain | Spain |
| Scotland | Scotland |
| Sweden | Sweden |
| Switzerland | Switzerland |
| Belgium | Belgium |
| Japan; japan | Japan |
| India; india | India |
| Denmark | Denmark |
| America | America |
| Singapore | Singapore |
| South Africa | South Africa |
| Austria | Austria |
| Finland | Finland |
| Norway | Norway |
| Israel | Israel |
| Italy | Italy |
| Malaysia | Malaysia |
| Brazil | Brazil |
| Philippines; Remote (philippines) | Philippines |
| Poland | Poland |
| China | China |
| Mexico | Mexico |
| Colombia | Colombia |
| Czech Republic | Czech Republic |
| Thailand | Thailand |
| Wales | Wales |
| Nigeria; Nigeria + UK | Nigeria |
| Argentina | Argentina |
| Great Britain | Great Britain |
| Hong Kong | Hong Kong |
| Greece | Greece |
| Puerto Rico | Puerto Rico |
| Romania | Romania |
| Taiwan | Taiwan |
| South Korea | South Korea |
| Portugal | Portugal |
| Pakistan | Pakistan |
| ISA | ISA |
| Luxembourg; Liechtenstein | Luxembourg |
| United States (I work from home and my clients are all over the US/Canada/PR; I am located in Canada but I work for a company in the US; I work for an US based company but I'm from Argentina. | United States (I work from home and my clients are all over the US/Canada/PR |
| Latvia | Latvia |
| 🇺🇸 | 🇺🇸 |
| For the United States government, but posted overseas; US govt employee overseas, country withheld; USA, but for foreign gov't | For the United States government, but posted overseas |
| Slovenia; Slovakia | Slovenia |
| Chile | Chile |
| Saudi Arabia | Saudi Arabia |
| Ghana | Ghana |
| Kenya | Kenya |
| Bermuda | Bermuda |
| Sri lanka | Sri lanka |
| Hungary | Hungary |
| U.A. | U.A. |
| United Arab Emirates | United Arab Emirates |
| Bangladesh | Bangladesh |
| Turkey | Turkey |
| USS; uS | USS |
| I.S. | I.S. |
| Vietnam | Vietnam |
| Remote | Remote |
| Lithuania | Lithuania |
| Indonesia | Indonesia |
| UK, remote | UK, remote |
| Uniter Statez | Uniter Statez |
| Bulgaria | Bulgaria |
| Estonia | Estonia |
| Morocco | Morocco |
| Zimbabwe | Zimbabwe |
| Croatia | Croatia |
| Cyprus | Cyprus |
| Myanmar | Myanmar |
| Kuwait | Kuwait |
| Contracts | Contracts |
| USA-- Virgin Islands | USA-- Virgin Islands |
| We don't get raises, we get quarterly bonuses, but they periodically asses income in the area you work, so I got a raise because a 3rd party assessment showed I was paid too little for the area we were located | We don't get raises, we get quarterly bonuses, but they periodically asses income in the area you work, so I got a raise because a 3rd party assessment showed I was paid too little for the area we were located |
| Canada, Ottawa, ontario | Canada, Ottawa, ontario |
| Global | Global |
| Worldwide (based in US but short term trips aroudn the world) | Worldwide (based in US but short term trips aroudn the world) |
| Trinidad and Tobago | Trinidad and Tobago |
| Cayman Islands | Cayman Islands |
| Can | Can |
| Rwanda | Rwanda |
| Currently finance | Currently finance |
| Serbia | Serbia |
| Russia | Russia |
| UXZ | UXZ |
| Catalonia | Catalonia |
| $2,175.84/year is deducted for benefits | $2,175.84/year is deducted for benefits |
| Italy (South) | Italy (South) |
| Jersey, Channel islands | Jersey, Channel islands |
| Virginia | Virginia |
| Afghanistan | Afghanistan |
| Hartford | Hartford |
| Japan, US Gov position | Japan, US Gov position |
| Mainland China | Mainland China |
| UK for U.S. company | UK for U.S. company |
| Cambodia | Cambodia |
| Eritrea | Eritrea |
| Cuba | Cuba |
| Cote d'Ivoire | Cote d'Ivoire |
| From Romania, but for an US based company | From Romania, but for an US based company |
| Somalia | Somalia |
| U.K. (northern England) | U.K. (northern England) |
| NL | NL |
| Sierra Leone | Sierra Leone |
| bonus based on meeting yearly goals set w/ my supervisor | bonus based on meeting yearly goals set w/ my supervisor |
| International | International |
| The Bahamas | The Bahamas |
| I earn commission on sales. If I meet quota, I'm guaranteed another 16k min. Last year i earned an additional 27k. It's not uncommon for people in my space to earn 100k+ after commission. | I earn commission on sales. If I meet quota, I'm guaranteed another 16k min. Last year i earned an additional 27k. It's not uncommon for people in my space to earn 100k+ after commission. |
| Costa Rica | Costa Rica |
| USAB | USAB |
| Qatar | Qatar |
| Panamá | Panamá |
| Austria, but I work remotely for a Dutch/British company | Austria, but I work remotely for a Dutch/British company |
| I was brought in on this salary to help with the EHR and very quickly was promoted to current position but compensation was not altered. | I was brought in on this salary to help with the EHR and very quickly was promoted to current position but compensation was not altered. |
| Congo | Congo |
| Uruguay | Uruguay |
| n/a (remote from wherever I want) | n/a (remote from wherever I want) |
| Uganda | Uganda |
| Malta | Malta |
| Africa | Africa |
| Ecuador | Ecuador |
| San Francisco | San Francisco |
| Ukraine | Ukraine |
| From New Zealand but on projects across APAC | From New Zealand but on projects across APAC |
| Y | Y |
| United y | United y |
| Isle of Man | Isle of Man |
| europe | europe |
| California | California |
| Jamaica | Jamaica |
| USD | USD |
| Jordan | Jordan |
| ARGENTINA BUT MY ORG IS IN THAILAND | ARGENTINA BUT MY ORG IS IN THAILAND |
| I work for a UAE-based organization, though I am personally in the US. | I work for a UAE-based organization, though I am personally in the US. |
| na | na |
| Policy | Policy |
| hong konh | hong konh |
| Company in Germany. I work from Pakistan. | Company in Germany. I work from Pakistan. |
| Bosnia and Herzegovina | Bosnia and Herzegovina |
| London | London |
| ss | ss |
| dbfemf | dbfemf |
| ibdia | ibdia |
| LOUTRELAND | LOUTRELAND |
| ff | ff |
| Tanzania | Tanzania |
| Italia | Italia |
| Egypt | Egypt |
| Liberia | Liberia |
| 1 | 1 |
| Zambia | Zambia |

---

## Postprocessing

No postprocessing changes applied.
