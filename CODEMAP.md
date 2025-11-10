# CODEMAP – google-access
_Quick function-level inventory_
_Updated: 2025-10-08_

---

## 🩺 Summary

| Category | Count | Notes |
|-----------|--------|-------|
| **Modules** | 7 | ingest, io, transform, utils, plus project-level file_transforms |
| **Functions complete** | 9 / 10 | 1 function pending (`download_item`) |
| **Projects linked** | 1 | `cacciamani-request` |
---

src/google_access
 ingest/                    # task-level pulls that call io/ and return clean in-memory objects (e.g. DataFrames)
    sheets.py
    [ ] get_google_sheets   # downloads data from table or tab in google sheets as a csv

 io/                        # API adapters (Google-only side effects)
   auth.py                  # get into google drive
    [x] authenticate        # authenticate google service account with SCOPES
    [x] build_service       # build service

   drive.py                 # navigate in drive
    [x] get_folder_items    # returns a list of dicts of folder_item: metadata

 transform/                 # pure transforms (no I/O)
    file_transforms.py
    [x] combine_pdfs        # combine multiple pdfs into one
    [x] remove_pages        # remove pages from pdf
    [ ] convert_jpg_to_pdf  # convert jpg to pdf

 utils/                     # helper functions

constants.py                # common constants
  [x] SCOPES : list
  [x] MIME_TYPES : dict

projects/member-data-consolidation/
  notebooks/
    01_build_member_master.ipynb    # notebook for creating master
  src/
    pipeline.py                     # loads sheets → transforms → CSV/DB export

---

## 🚧 Next Steps

- [ ] Implement `download_item` in `ingest.py`
- [ ] Add first transform under `transform/` (metadata normalization)
- [ ] Write smoke tests for `get_folder_items` and `combine_pdfs`
- [ ] Add automated CODEMAP summary generator to `tools/`
- [ ] Add project-level README with high-level flow diagram

---

_This document serves as the 30-second mental map of the repo. Update it as functions are created or refactored._
