# Workbook structure

File: `data/raw/Charpy_Impact_Test_Dataset.xlsx` (Materials Cloud record eny5v-www93 (DOI 10.24435/materialscloud:gh-za, issued 2024-12-19))

## Sheets

| name | state | dimensions | max_row | max_column | hidden_rows | hidden_columns | merged_ranges |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Charpy Data | visible | A1:BC4777 | 4777 | 55 | 0 | 0 | 7 |
| References | visible | A1:C107 | 107 | 3 | 0 | 0 | 0 |
| Column Descriptions | visible | A1:B55 | 55 | 2 | 0 | 0 | 0 |

## Data sheet layout

- Row 1: merged group headings; row 2: column names; records start at row 3.
- Column names with leading/trailing spaces: ['Material ', 'Test Temperature (C) ', 'Test Condition Statement ']
- Column groups: (no heading): 1 columns; Material Information: 2 columns; Material Composition (wt.%): 24 columns; Manufacturing and Treatment Information: 9 columns; Irradiation Conditions: 4 columns; Specimen Dimensions: 7 columns; Charpy Impact Test Conditions: 4 columns; Charpy Impact Test Properties: 4 columns

## Formula cells

- 439 formula cells, in columns ['Irradiation Dose (n/cm^2)'].
- Every formula is a constant of the form =(a*10^b) whose stored result equals its evaluation: True (0 problems).
- Distinct formulas: {'=(1.3*10^18)': 75, '=(1*10^19)': 72, '=(1.6*10^19)': 64, '=(8*10^19)': 28, '=(1.3*10^19)': 26, '=(2.7*10^19)': 26, '=(2.8*10^19)': 20, '=(3.4*10^19)': 19, '=(10*10^19)': 15, '=(3*10^19)': 13, '=(1.48*10^19)': 13, '=(2.7*10^18)': 12, '=(1.75*10^19)': 11, '=(3.1*10^19)': 10, '=(2.3*10^18)': 10, '=(2.52*10^19)': 9, '=(6.2*10^17)': 6, '=(3.9*10^18)': 6, '=(2.34*10^19)': 4}

## Reader cross-check (D-003)

- openpyxl normal vs read-only mode: 4777 vs 4777 rows, 0 differing cells.
- pandas.read_excel on the fluence column: dtype `object`, Python types {'str': 4336, 'int': 439}, 4336 empty cells returned as the text '' instead of missing. The pipeline therefore reads cells with openpyxl and assigns types explicitly.

## Column Descriptions sheet vs data headers

The sheet has no header row and lists descriptions in a different order from the data columns, so descriptions are matched by name through `curated_metadata.COLUMNS` (never by position).

| row | name in Column Descriptions | description (verbatim) | data header at same position |
| --- | --- | --- | --- |
| 1 | `'Reference'` | Reference ID to the paper where the data are extracted from, this ID links to the "References" sheet, where the Reference ID and the title of the paper are recorded | Reference |
| 2 | `'Material'` | Material used in the charpy test from each paper, such as SA 508, SA 533B steel | Material  |
| 3 | `'Material Group'` | Group of the material, the materials are divided into groups including Reactor Pressure Vessel Steels and Nuclear Structural Materials | Material Group |
| 4 | `'C (wt.%)'` | Weight percentage of the element in the material | C, wt.% |
| 5 | `'Si (wt.%)'` | Weight percentage of the element in the material | Si, wt.% |
| 6 | `'Mn (wt.%)'` | Weight percentage of the element in the material | Mn, wt.% |
| 7 | `'P (wt.%)'` | Weight percentage of the element in the material | P, wt.% |
| 8 | `'S (wt.%)'` | Weight percentage of the element in the material | S, wt.% |
| 9 | `'Ni (wt.%)'` | Weight percentage of the element in the material | Ni, wt.% |
| 10 | `'Cr (wt.%)'` | Weight percentage of the element in the material | Cr, wt.% |
| 11 | `'Mo (wt.%)'` | Weight percentage of the element in the material | Mo, wt.% |
| 12 | `'Al (wt.%)'` | Weight percentage of the element in the material | Al, wt.% |
| 13 | `'N (wt.%)'` | Weight percentage of the element in the material | N, wt.% |
| 14 | `'Ti (wt.%)'` | Weight percentage of the element in the material | Ti, wt.% |
| 15 | `'Fe (wt.%)'` | Weight percentage of the element in the material | Fe, wt.% |
| 16 | `'Nb (wt.%)'` | Weight percentage of the element in the material | Nb, wt.% |
| 17 | `'B (wt.%)'` | Weight percentage of the element in the material | B, wt.% |
| 18 | `'Cu (wt.%)'` | Weight percentage of the element in the material | Cu, wt.% |
| 19 | `'V (wt.%)'` | Weight percentage of the element in the material | V, wt.% |
| 20 | `'Zr (wt.%)'` | Weight percentage of the element in the material | Zr, wt.% |
| 21 | `'W (wt.%)'` | Weight percentage of the element in the material | W, wt.% |
| 22 | `'Sn (wt.%)'` | Weight percentage of the element in the material | Sn, wt.% |
| 23 | `'Co (wt.%)'` | Weight percentage of the element in the material | Co, wt.% |
| 24 | `'O (wt.%)'` | Weight percentage of the element in the material | O, wt,% |
| 25 | `'Ta (wt.%)'` | Weight percentage of the element in the material | Ta, wt.% |
| 26 | `'As (wt.%)'` | Weight percentage of the element in the material | As, wt% |
| 27 | `'Sb (wt.%)'` | Weight percentage of the element in the material | Sb, wt.% |
| 28 | `'Manufacturer'` | Manufacturer of the specimen | Manufacturer |
| 29 | `'Treatment'` | Treatment methods used for the material, such as ageing, austenitization, etc. | Treatment |
| 30 | `'Post Treatment Temperature (C)'` | Temperature applied after the treatment | Post Treatment Temperature (ºC) |
| 31 | `'Post Treatment Time (h)'` | Time duration of the post treatment process | Post Treatment Time (h) |
| 32 | `'Microstructure'` | Microstructure of the material | Cooling |
| 33 | `'Morphology '` | Morphology of the microstructure | Cooling Rate (ºC/min) |
| 34 | `'Grain size (um)'` | Grain size of the material | Miocrostructure |
| 35 | `'Irradiated Specimen'` | Whether the material is irradiated or not | Morphology |
| 36 | `'Irradiation Dose (n/cm^2)'` | Irradiation dose applied to the charpy specimen  | Grain size (um) |
| 37 | `'Irradiation Temperature (C)'` | Irradiation temperature during the irradiation process | Irradiated Specimen |
| 38 | `'Irradiation Time (hours)'` | Irradiation time of the irradiation process | Irradiation Dose (n/cm^2) |
| 39 | `'Length (mm)'` | Gauge length of the specimen | Irradiation Temperature (ºC) |
| 40 | `'Width (mm)'` | Width of the specimen | Irradiation Time (hours) |
| 41 | `'Thickness (mm)'` | Thickness of the specimen | Length (mm) |
| 42 | `'Notch Depth (mm)'` | The depth of the notch cut into the specimen for fracture testing | Width (mm) |
| 43 | `'Notch Angle (deg)'` | The angle at the apex of the notch in the test specimen | Thickness (mm) |
| 44 | `'Notch Root Radius (mm)'` | The radius of the curved portion at the base of the notch | Notch Depth (mm) |
| 45 | `'Notch Shape'` | The geometry of the notch  | Notch Angle (deg) |
| 46 | `'Test standard'` | The testing protocol or specification followed during the experiment, defined by an established standard organization  | Notch Root Radius (mm) |
| 47 | `'Test Temperature (C)'` | Charpy test environment temperature | Notch Shape |
| 48 | `'Orientation'` | Orientation of the specimen relative to the material's grain structure or rolling direction  | Test Standard |
| 49 | `'Cooling'` | Cooling method for the specimen preparation | Test Temperature (C)  |
| 50 | `'Cooling Rate (K/min)'` | The rate at which the temperature of the material decreases during the cooling process | Orientation |
| 51 | `'Test Condition Statement '` | Additional details about the testing environment | Test Condition Statement  |
| 52 | `'Impact energy (J)'` | The amount of energy absorbed by the material during an impact test. | Impact energy (J) |
| 53 | `'USE (J)'` | Upper Shelf Energy (USE), the maximum energy absorbed during the Charpy impact test | USE (J) |
| 54 | `'DBTT (C)'` | Ductile-to-Brittle Transition Temperature (DBTT), the temperature at which the material transitions from ductile to brittle behavior | DBTT (ºC) |
| 55 | `'DBTT Fitted Curve'` | Number of the fitted curve applied to the data for modeling or analysis | DBTT Fitted Curve |

- Curated description names not found in the sheet: none
