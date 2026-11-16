\# Testing Report



\## 1. Assessment Sample Evaluation



The application was evaluated using the 12 supplied assessment PDF documents (R01–R12).



| Evaluation Field | Accuracy |

|---|---:|

| Source Detection | 100% |

| Document Type | 100% |

| Expense Category | 100% |

| Vendor | 100% |

| Date | 100% |

| Amount | 100% |

| Currency | 100% |

| Reference Number | 100% |

| Processing Status | 100% |



\*\*Total documents:\*\* 12  

\*\*Processed documents:\*\* 12  

\*\*Total mismatches:\*\* 0



\## 2. Processing Status Verification



| Status | Expected | Actual |

|---|---:|---:|

| Done | 10 | 10 |

| Needs review | 1 | 1 |

| Unsupported | 1 | 1 |



\## 3. OCR Verification



The following scanned documents were processed using Tesseract OCR:



\- R03.pdf

\- R06.pdf

\- R08.pdf

\- R10.pdf



Digital PDFs were processed using PyMuPDF text extraction.



\## 4. Additional Robustness Tests



| Test Document | Expected Behaviour | Actual Result |

|---|---|---|

| CORRUPT\_TEST.pdf | Failed | Passed |

| EMPTY\_TEST.pdf | Failed | Passed |

| PASSWORD\_TEST.pdf | Failed | Passed |

| MULTIPAGE\_TEST.pdf | Extract document-stated total | Passed |



The multipage test correctly extracted the final total of 109.00 SGD.



\## 5. CSV Export Verification



\- Verified export of all 12 assessment documents.

\- Confirmed 11 output columns.

\- Confirmed R11 is correctly marked Unsupported.

\- Confirmed missing fields remain blank.

\- Confirmed R10 remains Needs review.



\## 6. Limitations



\- Rule-based classification may need improvements for unfamiliar document layouts.

\- OCR performance may decrease with poor-quality scans.

\- Unusual field formats may require manual review.

\- Confidence scores are not calibrated probabilities.



\## 7. Evaluation Scope



The reported 100% accuracy applies only to the 12 supplied assessment samples. It does not guarantee the same accuracy on unseen documents.

