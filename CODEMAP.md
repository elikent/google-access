# CODEMAP – google-access
_Quick function-level inventory_  
_Updated: 2025-10-07_

---

## 🩺 Summary

| Category | Count | Notes |
|-----------|--------|-------|
| **Modules** | 7 | ingest, io, transform, utils, plus project-level file_transforms |
| **Functions complete** | 9 / 10 | 1 function pending (`download_item`) |
| **Projects linked** | 1 | `cacciamani-request` |
---

## 📂 Source Structure and Function Inventory

 io/
   auth.py – get into google drive
    [x] authenticate – authenticate google service account with SCOPES
    [x] build_service – build service

   drive.py – navigate in drive
    [x] get_folder_items – returns a list of dicts of folder_item: metadata

 transform/
    (placeholder – to be implemented)

 utils/
  constants.py
    [x] SCOPES : list
    [x] MIME_TYPES : dict

  log_utils.py
    [x] report – report with message and level, optionally print
    [x] logging_config – configure global logging for app

  text_utils.py
    [x] remove_diacritics
    [x] cannon – canonicalize a filename or text string for matching


 src/
  google-access/
     ingest/
      ingest.py
        [] download_item - download item

     io/
       auth.py - get into google drive
        [x] authenticate - authenticate google service account with SCOPES 
        [x] build_service - build service

      drive.py - navigate in drive
        [x] get_folder_items - returns a list of dicts of folder_item: metadata

     transform/
     
     utils/
      constants.py
        [x] SCOPES : list
        [x] MIME_TYPES : dict

      log_utils.py
        [x] report - report with message and level. optionally print
        [x] logging_config - configure global logging for app

      text_utils.py
        [x] remove_diacritics
        [x] cannon - canonicalize a filename or text string for matching

projects\
  cacciamani-request\
    src\
      file_transforms.py
        [x] combine_pdfs - merge pdfs
        [x] remove_pages - remove pages from pdf

---

## 🧭 Notes

- `src/google-access/io/` holds low-level Google API integration (Drive, Auth).
- `src/utils/` contains reusable building blocks (logging, text, constants).
- `src/ingest/` is for pulling or downloading content.
- `src/transform/` is reserved for data transformations and normalization.
- `projects/cacciamani-request/` contains domain-specific operations.

---

## 🚧 Next Steps

- [ ] Implement `download_item` in `ingest.py`  
- [ ] Add first transform under `transform/` (metadata normalization)  
- [ ] Write smoke tests for `get_folder_items` and `combine_pdfs`  
- [ ] Add automated CODEMAP summary generator to `tools/`  
- [ ] Add project-level README with high-level flow diagram  

---

_This document serves as the 30-second mental map of the repo. Update it as functions are created or refactored._
