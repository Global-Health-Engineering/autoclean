# AutoClean Report

**Name of dataset:** Ask A Manager Salary Survey 2021 (Sample)  
**Filepath of messy dataset:** Data/Salary/Salary.csv  
**Filepath of cleaned dataset:** Data/Salary/Salary_Cleaned.csv  
**Generated:** 26.01.2026, 22:08:12

---

## Summary

- **Original shape:** 28187 rows × 18 columns
- **Final shape:** 190 rows × 2 columns
- **Total rows deleted:** 0
- **Total columns deleted:** 0
- **Total values imputed:** 0
- **Total outliers handled:** 0
- **Total semantic outliers detected:** 7
- **Total structural errors fixed:** 121

---

## Preprocessing

No completely empty rows or columns found respectfully removed.

---

## Semantic Outliers

### Overview

- **Column processed:** What country do you work in?
- **Given context:** Answers to question: What country do you work in? (abbreviations and possible typos are acceptable)
- **Threshold:** 0.1
- **Action:** nan
- **Unique values checked:** 190
- **Outliers detected:** 7

#### Detected Outliers

| Value | Confidence | Number of affected rows |
|-------|------------|-------------------------|
| dbfemf | 0.0 | 1 |
| bonus based on meeting yearly goals set w/ my supervisor | 0.0 | 1 |
| Y | 0.0 | 1 |
| We don't get raises, we get quarterly bonuses, but they periodically asses income in the area you work, so I got a raise because a 3rd party assessment showed I was paid too little for the area we were located | 0.0 | 1 |
| UXZ | 0.0 | 1 |
| San Francisco | 0.0 | 1 |
| Policy | 0.0 | 1 |

---

## Structural Errors

### Overview

- **Columns processed:** 2
- **Total values changed:** 121
- **Total unique values before:** 279
- **Total unique values after:** 173

### Column: What country do you work in?

- **Similarity method:** rapidfuzz
- **Clustering method:** connected_components
- **Threshold (connected components):** 0.81
- **Canonical selection:** most_frequent
- **Values changed:** 87
- **Unique values before:** 183
- **Unique values after:** 96

#### Clustering Results

| Original Values | Clustered to Canonical |
|-----------------|------------------------|
| 🇺🇸 | 🇺🇸 |
| Česká republika | Česká republika |
| usa; uSA; u.s.; Usat; Usa; UsA; USaa; USAB; USA; U.s.a.; U.s.; U.SA; U.S>; U.S.A.; U.S.A; U.S.; U.S | usa |
| us; uS; Us; US | us |
| united states of america; United states of america; United states of America; United States of america; United States of Americas; United States of American; United States of America; United States is America; United States Of America; United State of America; United Sates of America | united states of america |
| united states; united stated; united States; Untied States; Unted States; Uniyes States; Uniyed states; Unitied States; Unites states; Unites States; Uniter Statez; Unitef Stated; Uniteed States; United statew; United states; United Sttes; United Statws; United Status; United Statues; United Stattes; United Statss; United Statesp; United States; United Statees; United Stateds; United Stated; United Statea; United State; United Stares; United Sates; United STates; United  States; Unite States; Uniited States; UNited States; UNITED STATES; The United States | united states |
| united kingdom; Unites kingdom; United kingdom; United Kingdomk; United Kingdom.; United Kingdom; United Kindom | united kingdom |
| uk; Uk; UK | uk |
| the netherlands; the Netherlands; netherlands; The netherlands; The Netherlands | the netherlands |
| switzerland; Switzerland; SWITZERLAND | switzerland |
| ss | ss |
| spain; Spain | spain |
| singapore; Singapore | singapore |
| philippines | philippines |
| pakistan | pakistan |
| new zealand | new zealand |
| n/a (remote from wherever I want) | n/a (remote from wherever I want) |
| japan | japan |
| ireland | ireland |
| india | india |
| ibdia | ibdia |
| hong konh | hong konh |
| germany | germany |
| france | france |
| finland | finland |
| ff | ff |
| europe | europe |
| england | england |
| denmark | denmark |
| czech republic | czech republic |
| croatia | croatia |
| canada | canada |
| australia | australia |
| america | america |
| Zimbabwe | Zimbabwe |
| Zambia | Zambia |
| Worldwide (based in US but short term trips aroudn the world) | Worldwide (based in US but short term trips aroudn the world) |
| Wales, UK; Wales (UK) | Wales, UK |
| Wales (United Kingdom) | Wales (United Kingdom) |
| Wales | Wales |
| Virginia | Virginia |
| Vietnam | Vietnam |
| Uruguay | Uruguay |
| UnitedStates | UnitedStates |
| United y | United y |
| United States- Puerto Rico | United States- Puerto Rico |
| United States (I work from home and my clients are all over the US/Canada/PR | United States (I work from home and my clients are all over the US/Canada/PR |
| United Kingdom (England) | United Kingdom (England) |
| United Arab Emirates | United Arab Emirates |
| Ukraine | Ukraine |
| Uganda | Uganda |
| USS | USS |
| USD | USD |
| USA-- Virgin Islands | USA-- Virgin Islands |
| USA, but for foreign gov't | USA, but for foreign gov't |
| USA tomorrow | USA tomorrow |
| USA (company is based in a US territory, I work remote) | USA (company is based in a US territory, I work remote) |
| US of A | US of A |
| US govt employee overseas, country withheld | US govt employee overseas, country withheld |
| UK, remote | UK, remote |
| UK, but for globally fully remote company | UK, but for globally fully remote company |
| UK for U.S. company | UK for U.S. company |
| UK (Northern Ireland); U.K. (northern England) | UK (Northern Ireland) |
| UK (England) | UK (England) |
| UAE | UAE |
| UA | UA |
| U.K.; U.K | U.K. |
| U.A. | U.A. |
| U. S.; U. S | U. S. |
| Turkey | Turkey |
| Trinidad and Tobago | Trinidad and Tobago |
| The US | The US |
| The Bahamas | The Bahamas |
| Thailand | Thailand |
| Tanzania | Tanzania |
| Taiwan | Taiwan |
| Sweden | Sweden |
| Sri lanka; Sri Lanka | Sri lanka |
| South africa; South Africa | South africa |
| South Korea | South Korea |
| Somalia | Somalia |
| Slovenia | Slovenia |
| Slovakia | Slovakia |
| Sierra Leone | Sierra Leone |
| Serbia | Serbia |
| Scotland, UK | Scotland, UK |
| Scotland | Scotland |
| Saudi Arabia | Saudi Arabia |
| Rwanda | Rwanda |
| Russia | Russia |
| Romania | Romania |
| Remote (philippines) | Remote (philippines) |
| Remote | Remote |
| Qatar | Qatar |
| Puerto Rico | Puerto Rico |
| Portugal | Portugal |

### Column: What country do you work in?

- **Similarity method:** embeddings
- **Embedding model:** text-embedding-3-large
- **Clustering method:** connected_components
- **Threshold (connected components):** 0.66
- **Canonical selection:** most_frequent
- **Values changed:** 34
- **Unique values before:** 96
- **Unique values after:** 77

#### Clustering Results

| Original Values | Clustered to Canonical |
|-----------------|------------------------|
| 🇺🇸 | 🇺🇸 |
| Česká republika; czech republic | Česká republika |
| usa; us | usa |
| united states of america; united states; america; UnitedStates | united states |
| united kingdom; United Kingdom (England); UK (Northern Ireland); UK (England); U.K. | united kingdom |
| uk | uk |
| the netherlands | the netherlands |
| switzerland | switzerland |
| ss | ss |
| spain | spain |
| singapore | singapore |
| philippines | philippines |
| pakistan | pakistan |
| new zealand | new zealand |
| n/a (remote from wherever I want) | n/a (remote from wherever I want) |
| japan | japan |
| ireland | ireland |
| india | india |
| ibdia | ibdia |
| hong konh | hong konh |
| germany | germany |
| france | france |
| finland | finland |
| ff | ff |
| europe | europe |
| england | england |
| denmark | denmark |
| croatia | croatia |
| canada | canada |
| australia | australia |
| Zimbabwe | Zimbabwe |
| Zambia | Zambia |
| Worldwide (based in US but short term trips aroudn the world) | Worldwide (based in US but short term trips aroudn the world) |
| Wales, UK; Wales (United Kingdom); Wales | Wales, UK |
| Virginia | Virginia |
| Vietnam | Vietnam |
| Uruguay | Uruguay |
| United y | United y |
| United States- Puerto Rico; USA-- Virgin Islands; Puerto Rico | United States- Puerto Rico |
| United States (I work from home and my clients are all over the US/Canada/PR; USA (company is based in a US territory, I work remote) | United States (I work from home and my clients are all over the US/Canada/PR |
| United Arab Emirates; UAE | United Arab Emirates |
| Ukraine | Ukraine |
| Uganda | Uganda |
| USS | USS |
| USD | USD |
| USA, but for foreign gov't | USA, but for foreign gov't |
| USA tomorrow; US of A | USA tomorrow |
| US govt employee overseas, country withheld | US govt employee overseas, country withheld |
| UK, remote; UK, but for globally fully remote company | UK, remote |
| UK for U.S. company | UK for U.S. company |
| UA; U.A. | UA |
| U. S. | U. S. |
| Turkey | Turkey |
| Trinidad and Tobago | Trinidad and Tobago |
| The US | The US |
| The Bahamas | The Bahamas |
| Thailand | Thailand |
| Tanzania | Tanzania |
| Taiwan | Taiwan |
| Sweden | Sweden |
| Sri lanka | Sri lanka |
| South africa | South africa |
| South Korea | South Korea |
| Somalia | Somalia |
| Slovenia | Slovenia |
| Slovakia | Slovakia |
| Sierra Leone | Sierra Leone |
| Serbia | Serbia |
| Scotland, UK; Scotland | Scotland, UK |
| Saudi Arabia | Saudi Arabia |
| Rwanda | Rwanda |
| Russia | Russia |
| Romania | Romania |
| Remote (philippines) | Remote (philippines) |
| Remote | Remote |
| Qatar | Qatar |
| Portugal | Portugal |

---

## Postprocessing

### Precision Restoration (rounding)

No precision restoration (rounding) was applied in post-processing.

### Renamed Columns

Column renaming was not applied.
