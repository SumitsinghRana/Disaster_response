# app/utils/urgency.py  (replace your existing extract_locations function)

import spacy

nlp = spacy.load("en_core_web_sm")

# -------- URGENCY KEYWORDS --------
CRITICAL_KEYWORDS = [
    'dying', 'dead', 'trapped', 'urgent', 'emergency', 'critical',
    'help', 'sos', 'bleeding', 'unconscious', 'fire', 'collapse'
]

HIGH_KEYWORDS = [
    'injured', 'hurt', 'missing', 'flood', 'earthquake', 'need',
    'hospital', 'rescue', 'danger', 'damage', 'destroyed'
]

# -------- URGENCY FUNCTION --------
def get_urgency(text):
    text_lower = text.lower()
    
    if any(word in text_lower for word in CRITICAL_KEYWORDS):
        return 'Critical', 'danger'
    
    elif any(word in text_lower for word in HIGH_KEYWORDS):
        return 'High', 'warning'
    
    else:
        return 'Low', 'success'

# ---- Indian place name dictionary (expand this list freely) ----
INDIA_PLACES = {
    # States
    "uttar pradesh", "up", "bihar", "rajasthan", "gujarat", "maharashtra",
    "madhya pradesh", "mp", "west bengal", "karnataka", "tamil nadu",
    "andhra pradesh", "telangana", "kerala", "punjab", "haryana",
    "uttarakhand", "himachal pradesh", "jharkhand", "odisha", "assam",
    "chhattisgarh", "goa", "delhi", "jammu", "kashmir",

    # Major cities
    "mumbai", "delhi", "bangalore", "bengaluru", "chennai", "kolkata",
    "hyderabad", "pune", "ahmedabad", "jaipur", "lucknow", "kanpur",
    "nagpur", "surat", "patna", "indore", "bhopal", "ludhiana",
    "agra", "varanasi", "meerut", "allahabad", "prayagraj", "ghaziabad",
    "noida", "gurugram", "faridabad", "amritsar", "jodhpur", "kota",

    # Districts / smaller towns (add your region-specific ones here)
    "aligarh", "mathura", "bareilly", "moradabad", "saharanpur",
    "gorakhpur", "firozabad", "jhansi", "muzaffarnagar", "hapur",
    "etawah", "mainpuri", "budaun", "sitapur", "shahjahanpur",
    "lakhimpur", "hardoi", "unnao", "rae bareli", "raebareli",
    "fatehpur", "pratapgarh", "sultanpur", "ambedkar nagar",
    "gonda", "basti", "sant kabir nagar", "kushinagar", "deoria",
    "azamgarh", "mau", "ballia", "jaunpur", "ghazipur", "chandauli",
    "mirzapur", "sonbhadra", "hamirpur", "banda", "chitrakoot",
    "mahoba", "lalitpur", "jalaun", "orai", "etah", "kasganj",
    "hathras", "sambhal", "amroha", "rampur", "pilibhit", "lakhimpur kheri",
    "almora", "bageshwar", "chamoli", "champawat", "dehradun", "haridwar", "nainital", "pauri garhwal", "pithoragarh",
      "rudraprayag", "tehri garhwal", "udham singh nagar", "uttarkashi"
}

def extract_locations(text):
    found = []

    # Layer 1: spaCy NER (good for well-known cities)
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ('GPE', 'LOC', 'FAC'):
            found.append(ent.text.strip())

    # Layer 2: dictionary lookup (catches Indian districts/towns spaCy misses)
    text_lower = text.lower()
    for place in INDIA_PLACES:
        if place in text_lower:
            # Capitalize properly for display
            found.append(place.title())

    # Deduplicate (case-insensitive)
    seen = set()
    unique = []
    for loc in found:
        key = loc.lower()
        if key not in seen:
            seen.add(key)
            unique.append(loc)

    return unique