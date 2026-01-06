# AutoClean Report

**Dataset:** Drilling Data
**Generated:** 2026-01-06 14:47:49

---

## Summary

- **Original shape:** 157 rows × 136 columns
- **After preprocessing:** 157 rows × 70 columns
- **Total structural errors fixed:** 112

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

- **Columns processed:** 1
- **Total values changed:** 112

### drilling_rig_model

- **Similarity method:** embeddings
- **Clustering method:** affinity_propagation
- **Canonical selection:** llm
- **Embedding model:** text-embedding-3-large
- **Unique values before:** 90
- **Unique values after:** 12
- **Values changed:** 112

| Original Values | Canonical |
|-----------------|-----------|
| PRD 12 tonne, PRD, PRF 12 tonne, PRD 500, PRD 650, PRD, 650, PRD 650
48/21-22 | PRD 650 |
| KRD, Honda, KRD Honda | KRD Honda |
| KRD, 3875958-02 India HES, KRD,3875958,India,HES | KRD,3875958,India,HES |
| Ashokeleyland PHI 2012 model, Ashokeleland PHI 2012. Model, Ashokeland PHI 2012, Ashokeleland PHI, Ashokeleyland PHI2012 model, Ashokeleland PHI 2012, Ashokeleland PHI 2012 model, PHI,Ashokeleland 2012 model, Ashokeleland, Ashokeleland PHI2012 model, Ashokeleland PHI 2012 Model | Ashokeleland PHI 2012 model |
| AshokelandPHI 2012, AshokelandPHI,2012, Ashokeleland,PHI2012, AshokelelandPHI 2012, Ashokeleyland PHI, Ashokeleyland PHI 2012, Ashokeleyland,PHI,2012, AshokeleylandPHI2012, Ashokeleyland PH1 | AshokelandPHI 2012 |
| PHL Ashok Leyland, Ashok Leyland, Ashok Leyland
PRD 2518 il, Ashok Leyland
PRD Rig | Ashok Leyland |
| Ashokeleyland LG11000300, Ashokeleyland PRD,DZ 6337, Ashokeleyland,PRD,DZ 6337, Ashokeleyland,PRD,Dz 6337, Ashokeleyland,PRD ,DZ6337, Ashokeleyland,PRD,Dz6337, Ashoykeleyland PRD,DZ6337, Ashokeleyland PRD 6337, Ashok Reyland
PRD 650
48/21-22, Ashok Reyland
PRD | Ashokeleyland,PRD,DZ 6337 |
| Mounting car:Ashokeleyland NN9461,model PDR650,SL No:07/19/20, mounting car:Ashokeleyland NN9461,model PRD650,SLNo:07/19/20, Mounting Car Ashke Reland, NN 9461, Model PRD 650 | Mounting Car Ashke Reland, NN 9461, Model PRD 650 |
| ZA 6188,
Rig model:JCRDT600
Capacity-200mtr4"-12"
Top head rotary Drive-400kg-MTR,torque-120RPM, PRD Model;JCRDT 600,capacity-200mtr4"-12
Top head Rotary Drive-@400kg MTR,torque-120 RPM

Plate number ZA 6188, JCR DT609
Capacity_200mtr 4"-12" diameter hole
Top head rotery drive 400kg-MTR
Torque 120kpm
ZA6188, JCR DT-600
Drilling capacity 200 more,  4"-12" hole diameter
Pull up force 7,900kg, pull down force 5,400kg
Top head rotary drive  400kg- mtr torque 
0- 120 rpm
Plate Number ZA 6188, JCR DT -600
Drilling capacity -200 mtr,  4", 12"hole diameter 
7,900kg pull up force, 5,400 pull down force
400kg top head rotary drive
MTRD torque 0-120 rpm
Number plate ZA 6188, JCR DT-600
Drilling capacity -200 mtr, 4"-12" hole diameter 
7,900kg pull up force, 5,400kg pull down force
400g top head rotary drive- MTR torque, 0-200RPM, JCR DT-600
Drilling capacity -200 mtr, 4-12"hole diameter 
7900kg pull up force,  5,400kg pull down force 
400kg top head rotary drive-MTR torque,  
0-120RPM, JCR DT-600
Drilling capacity -200 mtr, 4"-12" hole diameter 
7,900kg pull up force, 5,400kg pull down force
400kg top head rotary drive -MTR torque, 0-120 RPM, JCR D-600
Drilling capacity 200 mtr, 4"-12" hole diameter
7,900kg pull up force,5,400kg pull down force
400kg top head rotary drive
MTR torque, 0-120RPM
Number Plate ZA 6188, JCR DT -600
Drilling capacity -200 mtr, 4"-12" hole diameter 
7,900kg pull up force, 5,400keep pull down force 
400kg top head rotary drive-MTR torque,  0-120 RPM, JCR DT -600
Drilling capacity -200 mtr, 4"-12" hole diameter 
7,900kg pull up force, 5 ,400kg pull down force 
400kg top head rotary drive-MTR torque, 0-120 RPM, JCR DT -600
Drilling capacity -200 mtr,  4"-12" hole diameter 
7,900kg pull down force,5,400kg pull up force
400kg top head rotary drive-MTR torque,  0-120RPM, JCR DT -600
Drilling capacity -200 mtr,  4"-12" hole diameter 
7,900kg pull up force, 5,400kg pull down force 
400kg top head rotary drive-MTR torque,  120 RPM, JCR DT-600
Drilling capacity -,200mtr4-12"hole diameter 
7,500kg pull up force,  5,400kg pull down force 
400kg Top head rotary drive-MTR torque ,120 RPM, JCR DT -600
Drilling capacity 200 mtr, 4"-12" hole diameter 
7, 900kg pull up force, 5 400kg pull down force  
400kg Top head rotary drive-MTR torque,  0-120 RPM, JCR DT -600
 Drilling capacity 200 mtr, 4"-12" hole diameter 
7,900kg pull up force, 5,400kg pull down 
400kg top head rotary drive-MTR torque, 0-120RPM, JCR DT -600
Drilling capacity 200 mtr, 4"-12" hole diameter 
7,900kg pull up force, 5,400kg pull down force 
400kg top head rotary drive-MTR torque, 0-120 RPM, JCR DT -600
Drilling capacity -200 mtr, 4"-12 hole diameter 
7,900kg pull up force, 5,400kg pull down force 
400kg Top head rotary drive-MTR torque,  0-120 RPM, JCR DT -600
Drilling capacity -200mtr, 4"-12" hole diameter 
7,900kg pull up force, 5,400kg pull down force 
400kg  top head rotary drive-MTR torque, 0-120 RPM, JCR DT -600
Drilling capacity 200mtr, 4"-12" hole diameter 
7,900kg pull up force, 5,400kg pull down force 
400kg top head rotary drive-MTR torque,  0-120 RPM, JCR DT -600
Drilling capacity 200mtr, 4"-12" hole diameter 
7,900kg pull up force,  5,400kg pull down force 
400kg top head rotary drive-MTR torque, 0 -120 rpm, JCR DT - 600
Drilling capacity 200mtr, 4"-12" hole diameter 
7,900kg pull up force, 5,400kg pull down force 
400kg top head rotary drive-MTR torque, 0-120 RPM, JCR DT -600
Drilling capacity  200mtr, 4"-12" hole diameter 
7,900kg pull up force,  5,400kg pull down force 
400kg Top head rotary drive-MTR torque,  0-120 RPM, JCR DT- 600 Drilling Capacity- 200mtr, 4"-12" hole diameter
700kg pull up force, 5,400kg pull down Force 400kg top head rotary drive. MTR torque, 0-200RPM, JCR DT-600, Drilling Capacity-200mtr, 4"-12" hole diameter
7,900kg pull up force, 5,400kg pull down Force.  400g top head rotary drive. MTR torque, 0-200 RPM, JCR DT-600 Drilling Capacity - 300mtr, 4"-12" hole diameter7,900kg pull up force, 5,400kg pull down Force.  400g top head rotary drive-MTR torque, 0-200RPM, JCR DT-600, Drilling Capacity 200mtr, 4"-12" hole diameter
700kg pull up force, 5400kg pull down force
400g top head rotary drive
MTR Torque, 0-200RPM, JCR DT-600 Drilling Capacity-200mtr, 4"-12" hole diameter, 
7900kg pull up force 5 400kg pull down force 400kg top head rotary drive MTR torque 0-200 RPM, JCR DT-600 Drilling Capacity -200mtr,  4"-12" hole diameter 
700kg pull up force ,  5 400kg pull down force  400g top head rotary drive 
MTR torque  200 rpm, JCR Dt 600 drilling capacity - 300mtr
4"-12" hole diameter
7900kg pull up force
5400kg pull down force
400gtoo head rotary drive
Matt Torque 0-200RPM, Prominent Drilling Rig,mounted on Reyland DAF.
Registration Number-BV6551
Pulling capacity 1000, Drilling rig type
Model no- LETO 350
Dril hole- 350meter depth
Drill dia-150-350mm
Year of make 2012
Truck mounted | JCR DT-600
Drilling capacity 200 more,  4"-12" hole diameter
Pull up force 7,900kg, pull down force 5,400kg
Top head rotary drive  400kg- mtr torque 
0- 120 rpm
Plate Number ZA 6188 |
| PDR, PDI | PDR |
| SC 400S, SC400s, SC400S, SC400S/PDI | SC400S |
| ELGI PG 1100s-300 (24 bar), ELGI PG 1100s - 300, ELGI PG 1100s-300, ELGI PG 600s 230 | ELGI PG 1100s-300 |

---

## Postprocessing

No postprocessing changes applied.
