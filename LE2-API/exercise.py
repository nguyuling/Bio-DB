# =============================================================================
#  FastAPI Exercise — Bioinformatics Gene Dataset
#  Run:  fastapi dev app.py
#  Docs: http://127.0.0.1:8000/docs
# =============================================================================

import pandas as pd
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query

# -----------------------------------------------------------------------------
# 1. Create the FastAPI app instance
#    title / description / version appear in the Swagger UI header
# -----------------------------------------------------------------------------
app = FastAPI(
    title="Gene Data API",
    description="A simple REST API to explore a local gene dataset (CSV).",
    version="1.0.0",
)


# -----------------------------------------------------------------------------
# 2. Load the CSV dataset ONCE at startup (not on every request)
#    This mimics what a DB connection would do in a real project.
#
#    pd.read_csv() gives us a DataFrame — we can filter it just like in
#    any data analysis script.
# -----------------------------------------------------------------------------
CSV_PATH = Path(__file__).parent / "genes.csv"

DF = pd.read_csv(CSV_PATH, dtype={"chromosome": str})  # keep chromosome as string
# ^ without dtype=str, pandas infers it as int64 which breaks string comparison


# =============================================================================
# ENDPOINTS
# =============================================================================

# -----------------------------------------------------------------------------
# 3. Root endpoint — sanity check
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    """Welcome message and dataset summary.""" #documentation
    return {
        "message": "Welcome to the Gene Data API!",
        "total_genes": len(DF),          # len(DataFrame) = number of rows
        "columns": list(DF.columns),     # show what fields are available
        "hint": "Visit /docs to explore all endpoints interactively.",
    }


# -----------------------------------------------------------------------------
# 4. PATH PARAMETER — /genes/{gene_id}
#
#    Path parameters are PART OF THE URL itself.
#    They identify a specific resource (like a primary key).
#
#    URL example:  GET /genes/BRCA1
# -----------------------------------------------------------------------------
@app.get("/genes/{gene_id}")
def get_gene_by_id(gene_id: str):
    """
    Retrieve a single gene record by its **gene_id**.

    - **gene_id**: the unique identifier in the dataset (e.g. `BRCA1`, `TP53`)
    - Returns 404 if the gene_id does not exist in the dataset.
    """
    # Boolean mask — case-insensitive match on the gene_id column
    mask = DF["gene_id"].str.upper() == gene_id.upper()
    result = DF[mask]

    if result.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Gene '{gene_id}' not found. Check /genes to see available IDs.",
        )

    # .iloc[0] → first matching row as a Series
    # .to_dict() → convert to plain Python dict for JSON serialisation
    return result.iloc[0].to_dict()


# -----------------------------------------------------------------------------
# 5. QUERY PARAMETERS — /genes
#
#    Query parameters appear AFTER the '?' in the URL.
#    They filter / paginate a collection — they are OPTIONAL by default.
#
#    URL examples:
#      GET /genes
#      GET /genes?organism=Homo sapiens
#      GET /genes?chromosome=17
#      GET /genes?organism=Homo sapiens&chromosome=17
#      GET /genes?limit=5
# -----------------------------------------------------------------------------
@app.get("/genes")
def list_genes(
    organism: str | None = Query(
        default=None,
        description="Filter by organism name (e.g. 'Homo sapiens', 'Mus musculus')",
    ),
    chromosome: str | None = Query(
        default=None,
        description="Filter by chromosome number (e.g. '17', '12')",
    ),
    limit: int = Query(
        default=10,
        ge=1,       # must be >= 1
        le=100,     # must be <= 100
        description="Maximum number of results to return (1–100)",
    ),
):
    """
    List genes from the dataset with optional filters.

    - **organism**: filter by organism (partial, case-insensitive match)
    - **chromosome**: filter by chromosome number (exact match)
    - **limit**: cap the number of results returned
    """
    result = DF.copy()   # start with the full DataFrame

    # Apply organism filter — str.contains() is case-insensitive partial match
    if organism:
        result = result[result["organism"].str.contains(organism, case=False, na=False)]

    # Apply chromosome filter — exact match (chromosome is stored as string)
    if chromosome:
        result = result[result["chromosome"] == chromosome]

    if result.empty:
        raise HTTPException(
            status_code=404,
            detail="No genes matched the given filters.",
        )

    # Apply limit then convert to list of dicts for JSON
    result = result.head(limit)

    return {
        "count": len(result),
        "filters": {"organism": organism, "chromosome": chromosome, "limit": limit},
        "data": result.to_dict(orient="records"),  # list of row dicts
    }


# -----------------------------------------------------------------------------
# 6. /organisms
#    A simple derived endpoint — shows unique organisms in the dataset.
#    No parameters needed;
# -----------------------------------------------------------------------------
@app.get("/organisms")
def list_organisms():
    """Return all unique organism names present in the dataset."""
    unique = sorted(DF["organism"].unique().tolist())
    return {"organisms": unique}