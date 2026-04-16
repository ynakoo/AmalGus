"""
AmalGus — Smart Product Discovery & Matching API
==================================================
A prototype B2B marketplace backend that uses semantic search (Sentence Transformers)
to match buyer queries against a catalog of glass & allied products.

Run:
    uvicorn main:app --reload
"""

import re
from typing import Optional

import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer

# ─────────────────────────────────────────────
# 1.  APP SETUP
# ─────────────────────────────────────────────
app = FastAPI(
    title="AmalGus — Smart Product Discovery",
    description="Semantic product matching for a B2B glass marketplace",
    version="0.1.0",
)

# Allow the React dev server (and any other origin) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# 2.  PRODUCT CATALOG  (12 realistic items)
# ─────────────────────────────────────────────
PRODUCTS = [
    {
        "id": 1,
        "name": "ClearShield Tempered Glass Panel",
        "category": "Tempered Glass",
        "specifications": {
            "thickness": "10mm",
            "size": "2440x1220mm",
            "color": "Clear",
            "coating": "None",
            "edge_finish": "Polished",
        },
        "supplier": "SafeGlass Industries",
        "price": 85.00,
        "image_url": "https://pplx-res.cloudinary.com/image/upload/pplx_search_images/01ff3a6ced172f4f320a2a23bd150ff75d3e37b9.jpg",
        "description": (
            "High-strength tempered glass panel ideal for frameless shower enclosures, "
            "glass partitions, and balustrades. Meets EN 12150 safety standards. "
            "Withstands thermal stress up to 250°C."
        ),
    },
    {
        "id": 2,
        "name": "OptiLam Laminated Safety Glass",
        "category": "Laminated Glass",
        "specifications": {
            "thickness": "6.38mm",
            "size": "2000x1000mm",
            "color": "Clear",
            "coating": "UV blocking interlayer",
            "edge_finish": "Seamed",
        },
        "supplier": "VitroShield Corp",
        "price": 62.50,
        "image_url": "https://pplx-res.cloudinary.com/image/upload/pplx_search_images/b92f7bca250b7c5b92e2341c2912bda8e7e5470a.jpg",
        "description": (
            "PVB-interlayer laminated glass offering excellent sound insulation and "
            "UV protection. Suitable for skylights, overhead glazing, and hurricane-prone "
            "areas. Retains fragments on breakage."
        ),
    },
    {
        "id": 3,
        "name": "ThermoSeal Insulated Glass Unit (IGU)",
        "category": "Insulated Glass Unit",
        "specifications": {
            "thickness": "24mm (6+12A+6)",
            "size": "1500x1200mm",
            "color": "Low-E coated",
            "coating": "Low-E on surface 2",
            "edge_finish": "Dual sealed",
        },
        "supplier": "EcoGlaze Systems",
        "price": 120.00,
        "image_url": "https://pplx-res.cloudinary.com/image/upload/pplx_search_images/30de73c1f0f2d9bf64b4a8770b8d1b39c124bf44.jpg",
        "description": (
            "Double-pane insulated glass unit with argon-filled cavity for superior "
            "thermal insulation. Reduces HVAC costs by up to 30%. Ideal for energy-"
            "efficient commercial facades and curtain walls."
        ),
    },
    {
        "id": 4,
        "name": "PrimeFloat Clear Float Glass",
        "category": "Float Glass",
        "specifications": {
            "thickness": "6mm",
            "size": "3210x2140mm",
            "color": "Clear",
            "coating": "None",
            "edge_finish": "Cut edge",
        },
        "supplier": "CrystalFlat Glass Ltd",
        "price": 28.00,
        "image_url": "https://pplx-res.cloudinary.com/image/upload/pplx_search_images/234d2be96c0e072e9127ffac4200440a366f71b3.jpg",
        "description": (
            "Standard clear float glass with excellent optical clarity. Raw material "
            "for further processing — tempering, laminating, or silvering. Suitable "
            "for windows, mirrors, and furniture applications."
        ),
    },
    {
        "id": 5,
        "name": "AluPro Sliding Door Hardware Kit",
        "category": "Aluminium Hardware",
        "specifications": {
            "thickness": "N/A",
            "size": "Fits doors up to 2400mm height",
            "color": "Anodized Silver",
            "coating": "Powder coated",
            "edge_finish": "N/A",
        },
        "supplier": "MetalCraft Solutions",
        "price": 145.00,
        "image_url": "https://pplx-res.cloudinary.com/image/upload/pplx_search_images/269d419ed26bade35f3cb0cf45a74e20b3228808.jpg",
        "description": (
            "Premium aluminium sliding door track-and-roller system with soft-close "
            "mechanism. Supports glass panels up to 120 kg. Corrosion-resistant "
            "anodized finish for interior and exterior use."
        ),
    },
    {
        "id": 6,
        "name": "FrostVeil Acid-Etched Glass",
        "category": "Decorative Glass",
        "specifications": {
            "thickness": "8mm",
            "size": "2440x1220mm",
            "color": "Frosted / Translucent",
            "coating": "Acid-etched single side",
            "edge_finish": "Polished",
        },
        "supplier": "ArtGlass Décor",
        "price": 72.00,
        "image_url": "https://pplx-res.cloudinary.com/image/upload/pplx_search_images/f3827e566ee0eb45effd2e52aaf67e96f0d7ded6.jpg",
        "description": (
            "Acid-etched glass providing a satin-smooth translucent finish for privacy "
            "without sacrificing light transmission. Popular for office partitions, "
            "bathroom enclosures, and decorative wall panels."
        ),
    },
    {
        "id": 7,
        "name": "SolarGuard Tinted Float Glass",
        "category": "Tinted Glass",
        "specifications": {
            "thickness": "6mm",
            "size": "3210x2140mm",
            "color": "Euro Grey",
            "coating": "Body-tinted",
            "edge_finish": "Cut edge",
        },
        "supplier": "CrystalFlat Glass Ltd",
        "price": 35.00,
        "image_url": "https://pplx-res.cloudinary.com/image/upload/pplx_search_images/7cd4db693b6c35a743c391aa47c8a3e24001f0c2.jpg",
        "description": (
            "Body-tinted float glass in Euro Grey that reduces solar heat gain and "
            "glare. Ideal for commercial facades, spandrel panels, and automotive "
            "glazing. Can be further tempered or laminated."
        ),
    },
    {
        "id": 8,
        "name": "MirrorPrime Silver-Coated Mirror",
        "category": "Mirror Glass",
        "specifications": {
            "thickness": "4mm",
            "size": "1830x1220mm",
            "color": "Silver reflective",
            "coating": "Silver + copper + protective paint",
            "edge_finish": "Bevelled",
        },
        "supplier": "ReflectPro Industries",
        "price": 42.00,
        "image_url": "https://pplx-res.cloudinary.com/image/upload/pplx_search_images/9c5e0aac19833390a6ed6bea281ebc56e3f206ba.jpg",
        "description": (
            "High-definition silver mirror with copper-backed moisture protection. "
            "Suitable for bathrooms, wardrobes, gyms, and commercial interiors. "
            "Bevelled edges add a premium decorative touch."
        ),
    },
    {
        "id": 9,
        "name": "AluFrame Curtain Wall Profile",
        "category": "Aluminium Hardware",
        "specifications": {
            "thickness": "N/A",
            "size": "6000mm lengths",
            "color": "RAL 7016 Anthracite Grey",
            "coating": "PVDF coated",
            "edge_finish": "N/A",
        },
        "supplier": "MetalCraft Solutions",
        "price": 210.00,
        "image_url": "https://pplx-res.cloudinary.com/image/upload/pplx_search_images/b20b3fb64bb924349185fa0219d34c2256043705.jpg",
        "description": (
            "Structural aluminium mullion profile for unitized curtain wall systems. "
            "PVDF coating ensures weather resistance for 25+ years. Thermally broken "
            "design for enhanced insulation."
        ),
    },
    {
        "id": 10,
        "name": "FireLite Wired Safety Glass",
        "category": "Safety Glass",
        "specifications": {
            "thickness": "7mm",
            "size": "1500x1000mm",
            "color": "Clear with wire mesh",
            "coating": "None",
            "edge_finish": "Seamed",
        },
        "supplier": "SafeGlass Industries",
        "price": 55.00,
        "image_url": "https://pplx-res.cloudinary.com/image/upload/pplx_search_images/868a8bd002f4345b55c166306330d84559715a1c.jpg",
        "description": (
            "Wire-reinforced safety glass rated for 60-minute fire resistance. "
            "Prevents flame and smoke passage. Used in fire-rated doors, windows, "
            "and stairwell enclosures per building fire codes."
        ),
    },
    {
        "id": 11,
        "name": "BackSplash Lacquered Glass Panel",
        "category": "Decorative Glass",
        "specifications": {
            "thickness": "6mm",
            "size": "2440x1220mm",
            "color": "Pure White (RAL 9010)",
            "coating": "Back-painted lacquer",
            "edge_finish": "Polished",
        },
        "supplier": "ArtGlass Décor",
        "price": 68.00,
        "image_url": "https://pplx-res.cloudinary.com/image/upload/pplx_search_images/850084f725b82288c2e9e86475a1dce7f791d2b0.jpg",
        "description": (
            "Back-painted lacquered glass in Pure White, perfect for kitchen "
            "backsplashes, feature walls, and cladding. Scratch-resistant baked "
            "finish ensures long-lasting color vibrancy."
        ),
    },
    {
        "id": 12,
        "name": "StructoGlass Structural Glazing Sealant",
        "category": "Sealants & Accessories",
        "specifications": {
            "thickness": "N/A",
            "size": "600 mL cartridge",
            "color": "Black",
            "coating": "N/A",
            "edge_finish": "N/A",
        },
        "supplier": "BondTech Chemicals",
        "price": 18.50,
        "image_url": "https://pplx-res.cloudinary.com/image/upload/pplx_search_images/6266f0bf5e296a833795df1df66137f2f3c86867.jpg",
        "description": (
            "Two-part silicone structural glazing sealant for bonding glass to "
            "aluminium frames in curtain wall and structural glazing systems. "
            "UV-stable, weatherproof, and meets ASTM C1184 requirements."
        ),
    },
]


# ─────────────────────────────────────────────
# 3.  EMBEDDING ENGINE
# ─────────────────────────────────────────────

# We load the model once at import time so it's ready when the first request hits.
print("⏳  Loading embedding model (all-MiniLM-L6-v2) …")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅  Model loaded.")


def _product_text(product: dict) -> str:
    """
    Flatten a product dict into a single text string that captures all
    searchable attributes.  This is what gets embedded.
    """
    specs = product["specifications"]
    spec_parts = " | ".join(f"{k}: {v}" for k, v in specs.items() if v != "N/A")
    return (
        f"{product['name']}. "
        f"Category: {product['category']}. "
        f"Specs — {spec_parts}. "
        f"{product['description']}"
    )


# Pre-compute product text representations and their embeddings at startup.
PRODUCT_TEXTS = [_product_text(p) for p in PRODUCTS]
PRODUCT_EMBEDDINGS = model.encode(PRODUCT_TEXTS, normalize_embeddings=True)
print(f"📦  Embedded {len(PRODUCTS)} products  (shape {PRODUCT_EMBEDDINGS.shape})")


# ─────────────────────────────────────────────
# 4.  REQUEST / RESPONSE SCHEMAS
# ─────────────────────────────────────────────

class MatchRequest(BaseModel):
    """Incoming search payload."""
    query: str = Field(..., min_length=3, examples=["6mm clear glass for office partitions"])
    category: Optional[str] = Field(None, examples=["Tempered Glass"])
    max_price: Optional[float] = Field(None, ge=0, examples=[100.0])
    thickness: Optional[str] = Field(None, examples=["6mm"])


class MatchResult(BaseModel):
    """A single product match returned to the caller."""
    product_name: str
    category: str
    supplier: str
    price: float
    image_url: str
    match_score: float = Field(..., ge=0, le=100)
    matched_attributes: list[str]
    explanation: str
    specifications: dict


class MatchResponse(BaseModel):
    """Top-level response wrapper."""
    query: str
    results: list[MatchResult]


# ─────────────────────────────────────────────
# 5.  MATCHING & EXPLANATION LOGIC
# ─────────────────────────────────────────────

def _cosine_scores(query_embedding: np.ndarray) -> np.ndarray:
    """
    Compute cosine similarity between *query_embedding* and every product.
    Because embeddings are already L2-normalized, dot product = cosine sim.
    """
    return query_embedding @ PRODUCT_EMBEDDINGS.T


# --- Keyword / attribute helpers for explanation generation ----------------

_THICKNESS_RE = re.compile(r"(\d+(?:\.\d+)?)\s*mm", re.IGNORECASE)
_CATEGORY_KEYWORDS = {
    "tempered": "Tempered Glass",
    "laminated": "Laminated Glass",
    "igu": "Insulated Glass Unit",
    "insulated": "Insulated Glass Unit",
    "float": "Float Glass",
    "tinted": "Tinted Glass",
    "mirror": "Mirror Glass",
    "decorative": "Decorative Glass",
    "frosted": "Decorative Glass",
    "safety": "Safety Glass",
    "fire": "Safety Glass",
    "aluminium": "Aluminium Hardware",
    "aluminum": "Aluminium Hardware",
    "hardware": "Aluminium Hardware",
    "sealant": "Sealants & Accessories",
}

_USE_CASE_KEYWORDS = {
    "partition": "partitions",
    "facade": "facades",
    "curtain wall": "curtain walls",
    "shower": "shower enclosures",
    "skylight": "skylights",
    "kitchen": "kitchen applications",
    "backsplash": "kitchen backsplashes",
    "bathroom": "bathroom applications",
    "balustrade": "balustrades",
    "door": "doors",
    "window": "windows",
    "furniture": "furniture",
    "interior": "interior applications",
    "exterior": "exterior applications",
    "energy": "energy efficiency",
    "thermal": "thermal insulation",
    "fire": "fire resistance",
    "sound": "sound insulation",
    "acoustic": "sound insulation",
    "uv": "UV protection",
    "privacy": "privacy",
    "decorative": "decorative use",
}


def _extract_query_attributes(query: str) -> dict:
    """
    Pull structured attributes out of the free-text query so we can
    compare them against product specs and build explanations.
    """
    q = query.lower()
    attrs: dict = {}

    # Thickness
    m = _THICKNESS_RE.search(query)
    if m:
        attrs["thickness"] = m.group(0).lower().replace(" ", "")

    # Category hints
    for kw, cat in _CATEGORY_KEYWORDS.items():
        if kw in q:
            attrs["category"] = cat
            break

    # Use-case hints
    matched_uses = []
    for kw, label in _USE_CASE_KEYWORDS.items():
        if kw in q:
            matched_uses.append(label)
    if matched_uses:
        attrs["use_cases"] = matched_uses

    # Color cues
    for color in ("clear", "grey", "gray", "green", "bronze", "blue", "white", "black", "frosted"):
        if color in q:
            attrs["color"] = color.capitalize()
            break

    return attrs


def _build_explanation(product: dict, query_attrs: dict) -> tuple[str, list[str]]:
    """
    Compare extracted query attributes against product specs and return
    a human-readable explanation string + list of matched attribute names.
    """
    reasons: list[str] = []
    matched_attrs: list[str] = []

    specs = product["specifications"]
    desc_lower = product["description"].lower()

    # Thickness match
    if "thickness" in query_attrs:
        qt = query_attrs["thickness"]
        if qt in specs.get("thickness", "").lower():
            reasons.append(f"Matches thickness ({qt})")
            matched_attrs.append("thickness")

    # Category match
    if "category" in query_attrs:
        if query_attrs["category"].lower() == product["category"].lower():
            reasons.append(f"Category match ({product['category']})")
            matched_attrs.append("category")

    # Color match
    if "color" in query_attrs:
        qc = query_attrs["color"].lower()
        if qc in specs.get("color", "").lower() or qc in desc_lower:
            reasons.append(f"{query_attrs['color']} glass requirement satisfied")
            matched_attrs.append("color")

    # Use-case matches
    if "use_cases" in query_attrs:
        for uc in query_attrs["use_cases"]:
            # Check if the use-case keyword appears in the product description
            uc_check = uc.split()[0].lower()  # first word of the label
            if uc_check in desc_lower or uc_check in product["name"].lower():
                reasons.append(f"Suitable for {uc}")
                matched_attrs.append(uc)

    # Fallback: if no specific attribute matched, mention the category
    if not reasons:
        reasons.append(f"Semantically relevant ({product['category']})")
        matched_attrs.append("semantic_match")

    return ", ".join(reasons), matched_attrs


# ─────────────────────────────────────────────
# 6.  API ENDPOINTS
# ─────────────────────────────────────────────

@app.get("/", tags=["Health"])
def health_check():
    """Quick sanity check — proves the server is up."""
    return {
        "service": "AmalGus Smart Product Discovery",
        "status": "running",
        "products_indexed": len(PRODUCTS),
    }


@app.post("/match", response_model=MatchResponse, tags=["Matching"])
def match_products(req: MatchRequest):
    """
    Core endpoint: accepts a natural-language query (and optional filters)
    and returns the top-5 semantically similar products.
    """

    # --- Step 1: Embed the query -------------------------------------------
    query_embedding = model.encode([req.query], normalize_embeddings=True)

    # --- Step 2: Cosine similarity with every product ----------------------
    scores = _cosine_scores(query_embedding).flatten()  # shape (12,)

    # --- Step 3: Apply optional hard filters --------------------------------
    # Build a boolean mask — True means "keep this product"
    mask = np.ones(len(PRODUCTS), dtype=bool)

    for idx, product in enumerate(PRODUCTS):
        # Category filter (case-insensitive substring)
        if req.category and req.category.lower() not in product["category"].lower():
            mask[idx] = False

        # Max price filter
        if req.max_price is not None and product["price"] > req.max_price:
            mask[idx] = False

        # Thickness filter (substring match in the specs)
        if req.thickness and req.thickness.lower() not in product["specifications"].get("thickness", "").lower():
            mask[idx] = False

    # Zero out scores of filtered-out products so they won't appear in top-K
    scores = scores * mask

    # --- Step 4: Rank and pick top 5 ----------------------------------------
    top_indices = np.argsort(scores)[::-1][:5]

    # --- Step 5: Build results with explanations ----------------------------
    query_attrs = _extract_query_attributes(req.query)
    results: list[MatchResult] = []

    for i in top_indices:
        score_pct = round(float(scores[i]) * 100, 2)
        if score_pct <= 0:
            continue  # skip filtered-out products with zero score

        product = PRODUCTS[i]
        explanation, matched_attrs = _build_explanation(product, query_attrs)

        results.append(
            MatchResult(
                product_name=product["name"],
                category=product["category"],
                supplier=product["supplier"],
                price=product["price"],
                image_url=product.get("image_url", ""),
                match_score=score_pct,
                matched_attributes=matched_attrs,
                explanation=explanation,
                specifications=product["specifications"],
            )
        )

    return MatchResponse(query=req.query, results=results)
