# AutoClean Report

**Dataset:** Drilling Data
**Generated:** 2026-01-07 00:17:17

---

## Summary

- **Original shape:** 157 rows × 136 columns
- **After preprocessing:** 157 rows × 70 columns
- **Total structural errors fixed:** 115

---

## Preprocessing

- **Empty columns removed:** 66
- **Columns renamed:** 3

| Original | New |
|----------|-----|
|  date_casing_installation   | _date_casing_installation_ |
| casing_connection_type   | casing_connection_type_ |
|  gravel_pack_quality | _gravel_pack_quality |

---

## Duplicates

- **Duplicate columns removed:** 6

---

## Structural Errors

- **Columns processed:** 2
- **Total values changed:** 115

### drilling_contractor

- **Similarity method:** rapidfuzz
- **Clustering method:** hierarchical
- **Canonical selection:** llm
- **Threshold:** 0.8
- **Unique values before:** 55
- **Unique values after:** 38
- **Values changed:** 28

#### Clustering Results

| Original Values | Canonical |
|-----------------|-----------|
| Blue Water Drilling Ltd; Blue Water Drilling  Ltd | Blue Water Drilling Ltd |
| Saifro Ltd; Saifro Limited | Saifro Limited |
| Rymech | Rymech |
| OG Madzi | OG Madzi |
| Nditha Drilling and Civil Contractor; Nditha  Drilling and Civil Contractors; Nditha Drilling  and Civil Contractors; Nditha Civil and Drilling Contractors; Nditha Drilling and Civil Contractors | Nditha Drilling and Civil Contractors |
| China Gansu | China Gansu |
| OG Madzi Drilling Company; OG MADZI Drilling Company | OG Madzi Drilling Company |
| Saifro Limited Malawi; Saifro Malawi Limited | Saifro Malawi Limited |
| Water Way Malawi; Water Way  Malawi; Way Water Malawi | Water Way Malawi |
| Nditha Drilling and Civil contractors; Nditha Drilling  and Civil contrators | Nditha Drilling and Civil contractors |
| GIMM water experts and drilling; GIMM Water experts and drilling | GIMM Water experts and drilling |
| Dec Construction | Dec Construction |
| OG Madzi Drilling; OG Madzi Drillers | OG Madzi Drilling |
| Saifro Malawi | Saifro Malawi |
| Blue Water Drilling Company; Blue water Drilling Company | Blue Water Drilling Company |
| Blue water drilling Ltd | Blue water drilling Ltd |
| Dec construction; Dec construction Limited | Dec construction Limited |
| Blue water | Blue water |
| Eazy borehole drillers | Eazy borehole drillers |
| GIMM; GIMME | GIMME |
| China Gansu Engineering Co. | China Gansu Engineering Co. |
| Patel and Ghodaniya; Patel and Godhaniya | Patel and Ghodaniya |
| Blue water Drilling company | Blue water Drilling company |
| Mushtaq
Of OG Madzi Drillinv | Mushtaq
Of OG Madzi Drillinv |
| OG MADZI drilling comopany | OG MADZI drilling comopany |
| OG Madzi Construction | OG Madzi Construction |
| OG MADZI | OG MADZI |
| EAZY Drilling Copmany | EAZY Drilling Copmany |
| Eazy borehole drilling Company | Eazy borehole drilling Company |
| EASY BOREHOLE DRILLING COMPANY | EASY BOREHOLE DRILLING COMPANY |
| Eazy borehole Drilling company | Eazy borehole Drilling company |
| Saifro Limited Company | Saifro Limited Company |
| Saifro | Saifro |
| Saifro Drilling Company | Saifro Drilling Company |
| Nditha drilling and civil contractors | Nditha drilling and civil contractors |
| GIMM water experts and Drilling | GIMM water experts and Drilling |
| Nyaungano Drilling company | Nyaungano Drilling company |
| Mthunzi Wa Kachere | Mthunzi Wa Kachere |

### drilling_contractor

- **Similarity method:** embeddings
- **Clustering method:** affinity_propagation
- **Canonical selection:** llm
- **Embedding model:** text-embedding-3-large
- **Unique values before:** 38
- **Unique values after:** 11
- **Values changed:** 87

#### Clustering Results

| Original Values | Canonical |
|-----------------|-----------|
| Blue Water Drilling Company; Blue Water Drilling Ltd; Blue water drilling Ltd; Nyaungano Drilling company; Blue water; Blue water Drilling company | Blue Water Drilling Ltd |
| Saifro Limited; Saifro Limited Company; Saifro Malawi; Saifro Malawi Limited; Saifro; Saifro Drilling Company | Saifro Malawi Limited |
| OG Madzi; OG Madzi Drilling Company; Mushtaq
Of OG Madzi Drillinv; OG Madzi Drilling; OG MADZI drilling comopany; OG Madzi Construction; OG MADZI | OG Madzi Drilling |
| Nditha Drilling and Civil Contractors; Nditha Drilling and Civil contractors; Nditha drilling and civil contractors | Nditha Drilling and Civil Contractors |
| Rymech | Rymech |
| China Gansu; China Gansu Engineering Co. | China Gansu Engineering Co. |
| Dec Construction; Dec construction Limited | Dec Construction |
| GIMM Water experts and drilling; GIMME; GIMM water experts and Drilling | GIMM Water experts and drilling |
| EAZY Drilling Copmany; Eazy borehole drillers; Eazy borehole drilling Company; EASY BOREHOLE DRILLING COMPANY; Eazy borehole Drilling company | Eazy borehole drilling Company |
| Water Way Malawi; Mthunzi Wa Kachere | Mthunzi Wa Kachere |
| Patel and Ghodaniya | Patel and Ghodaniya |

---

## Postprocessing

No postprocessing changes applied.
