# Checksum verification

All vendored raw files match their recorded SHA-256 values, and each workbook's MD5 matches the value published in its Materials Cloud record.

| file | check | expected | actual | ok |
| --- | --- | --- | --- | --- |
| raw/Charpy_Impact_Test_Dataset.xlsx | SHA-256 vs data/CHECKSUMS.sha256 | 37bc6526218e2260b9d11f15d09e8ebf5d01e863242aed520d28bdb4c5cb89db | 37bc6526218e2260b9d11f15d09e8ebf5d01e863242aed520d28bdb4c5cb89db | True |
| raw/files_description.md | SHA-256 vs data/CHECKSUMS.sha256 | 156a865126cf64e77ba5301db88d1769d32fb09c3c107ebfd3ffcb3e1ccf003c | 156a865126cf64e77ba5301db88d1769d32fb09c3c107ebfd3ffcb3e1ccf003c | True |
| raw/materialscloud_record_eny5v-www93.json | SHA-256 vs data/CHECKSUMS.sha256 | 4b3827cea57eab8d558c04fda1a1fea09555ac8b18c3f7d54aa3ad52a02d535e | 4b3827cea57eab8d558c04fda1a1fea09555ac8b18c3f7d54aa3ad52a02d535e | True |
| raw/alternate_record_q4x6v-dyt25/Charpy_Impact_Test_Dataset.xlsx | SHA-256 vs data/CHECKSUMS.sha256 | 2187109a76a8153245ae4fee003b12d3fd452900c2e9c16e7deea71a8786f23d | 2187109a76a8153245ae4fee003b12d3fd452900c2e9c16e7deea71a8786f23d | True |
| raw/alternate_record_q4x6v-dyt25/files_description.md | SHA-256 vs data/CHECKSUMS.sha256 | 156a865126cf64e77ba5301db88d1769d32fb09c3c107ebfd3ffcb3e1ccf003c | 156a865126cf64e77ba5301db88d1769d32fb09c3c107ebfd3ffcb3e1ccf003c | True |
| raw/alternate_record_q4x6v-dyt25/materialscloud_record_q4x6v-dyt25.json | SHA-256 vs data/CHECKSUMS.sha256 | e81b5d4c0218c6e3c61c696e6c8849ac44890bb241096225b2db28ec441803a2 | e81b5d4c0218c6e3c61c696e6c8849ac44890bb241096225b2db28ec441803a2 | True |
| LICENSE-CC-BY-4.0.txt | SHA-256 vs data/CHECKSUMS.sha256 | 9ba9550ad48438d0836ddab3da480b3b69ffa0aac7b7878b5a0039e7ab429411 | 9ba9550ad48438d0836ddab3da480b3b69ffa0aac7b7878b5a0039e7ab429411 | True |
| raw/files_description.md | MD5 vs archive record eny5v-www93 | 78e8d2c3d2c3333c52822ceea34033a4 | 78e8d2c3d2c3333c52822ceea34033a4 | True |
| raw/Charpy_Impact_Test_Dataset.xlsx | MD5 vs archive record eny5v-www93 | a7e2f05e92baa298c8043569d8ab8b26 | a7e2f05e92baa298c8043569d8ab8b26 | True |
| raw/alternate_record_q4x6v-dyt25/Charpy_Impact_Test_Dataset.xlsx | MD5 vs archive record q4x6v-dyt25 | d4002dd0bfc7d029d254851b985bd05b | d4002dd0bfc7d029d254851b985bd05b | True |
| raw/alternate_record_q4x6v-dyt25/files_description.md | MD5 vs archive record q4x6v-dyt25 | 78e8d2c3d2c3333c52822ceea34033a4 | 78e8d2c3d2c3333c52822ceea34033a4 | True |
