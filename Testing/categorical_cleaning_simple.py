"""
Categorical Data Cleaning mit Affinity Propagation
Einfache Version - nur die essentiellen Funktionen
"""

import numpy as np
from sklearn.cluster import AffinityPropagation


# =============================================================================
# ÄHNLICHKEITSFUNKTIONEN
# =============================================================================

def levenshtein_similarity(a, b):
    """Levenshtein-Distanz für Tippfehler"""
    if len(a) < len(b):
        a, b = b, a
    if len(b) == 0:
        return 0.0
    
    previous_row = range(len(b) + 1)
    for i, ca in enumerate(a):
        current_row = [i + 1]
        for j, cb in enumerate(b):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (ca != cb)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    distance = previous_row[-1]
    max_len = max(len(a), len(b))
    return 1 - (distance / max_len)


def jaccard_similarity(a, b):
    """Jaccard-Index für Wortumstellungen"""
    s1 = set(a.replace(',', '').split())
    s2 = set(b.replace(',', '').split())
    
    if len(s1.union(s2)) > 0:
        return len(s1.intersection(s2)) / len(s1.union(s2))
    return 0.0


def ngram_similarity(a, b, n=2):
    """Character N-Grams für Teilstring-Matches"""
    def get_ngrams(text, n):
        if len(text) < n:
            return set([text])
        return set(text[i:i+n] for i in range(len(text)-n+1))
    
    if len(a) < n and len(b) < n:
        return levenshtein_similarity(a, b)
    
    ngrams_a = get_ngrams(a, n)
    ngrams_b = get_ngrams(b, n)
    
    if len(ngrams_a.union(ngrams_b)) == 0:
        return 0.0
    
    return len(ngrams_a.intersection(ngrams_b)) / len(ngrams_a.union(ngrams_b))


def is_abbreviation(short, long):
    """Erkennt Abkürzungen (NY → New York, LA → Los Angeles)"""
    short_clean = short.replace('.', '').replace(',', '').upper().strip()
    long_clean = long.upper().strip()
    
    if not short_clean or not long_clean:
        return False
    
    # Initialen (NY für New York)
    words = long_clean.split()
    if len(words) > 1:
        initials = ''.join([w[0] for w in words if w])
        if short_clean == initials:
            return True
    
    # Teilstring (LA in Los Angeles)
    if short_clean in long_clean.replace(' ', '') and len(short_clean) >= 2:
        return True
    
    return False


def string_similarity(s1, s2):
    """
    Kombinierte Ähnlichkeitsmetrik
    
    Behandelt:
    - Tippfehler (Levenshtein)
    - Wortumstellungen (Jaccard)
    - Teilmatches (N-Gram)
    - Abkürzungen (is_abbreviation)
    - Groß/Kleinschreibung (automatisch)
    """
    s1_lower = s1.lower().strip()
    s2_lower = s2.lower().strip()
    
    # Exakt gleich
    if s1_lower == s2_lower:
        return 1.0
    
    # Abkürzung
    if is_abbreviation(s1_lower, s2_lower) or is_abbreviation(s2_lower, s1_lower):
        return 0.85
    
    # Kombiniere Metriken
    lev = levenshtein_similarity(s1_lower, s2_lower)
    jac = jaccard_similarity(s1_lower, s2_lower)
    ngram = ngram_similarity(s1_lower, s2_lower, n=2)
    
    return 0.35 * jac + 0.35 * lev + 0.30 * ngram


# =============================================================================
# HAUPT-CLEANING-FUNKTION
# =============================================================================

def clean_categorical_data(data, preference=-0.5, min_similarity=0.5):
    """
    Bereinigt kategoriale Daten durch Clustering
    
    Parameters:
    -----------
    data : list
        Liste mit kategorialen Daten (z.B. Städtenamen)
    preference : float
        Kontrolliert Anzahl der Cluster
        Niedriger = weniger Cluster (z.B. -1.0)
        Höher = mehr Cluster (z.B. -0.2)
    min_similarity : float
        Minimale Ähnlichkeit für Cluster-Zugehörigkeit (0-1)
        Höher = konservativer
    
    Returns:
    --------
    cleaned_data : list
        Bereinigte Daten
    mapping : dict
        Original → Bereinigt Mapping
    """
    
    # Unique values
    unique_values = list(set(data))
    n = len(unique_values)
    
    # Similarity matrix
    similarity_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            sim = string_similarity(unique_values[i], unique_values[j])
            similarity_matrix[i, j] = sim
            similarity_matrix[j, i] = sim
    
    # Affinity matrix
    affinity_matrix = -((1 - similarity_matrix) ** 2)
    
    # Clustering
    ap = AffinityPropagation(
        affinity='precomputed',
        preference=preference,
        damping=0.9,
        random_state=42,
        max_iter=500
    )
    ap.fit(affinity_matrix)
    
    # Mapping erstellen
    labels = ap.labels_
    exemplar_indices = ap.cluster_centers_indices_
    
    mapping = {}
    for i, value in enumerate(unique_values):
        cluster_id = labels[i]
        exemplar_idx = exemplar_indices[cluster_id]
        exemplar_value = unique_values[exemplar_idx]
        
        # Validierung
        similarity = string_similarity(value, exemplar_value)
        if similarity >= min_similarity:
            mapping[value] = exemplar_value
        else:
            mapping[value] = value  # Behalte Original
    
    # Auf Daten anwenden
    cleaned_data = [mapping[val] for val in data]
    
    return cleaned_data, mapping


# =============================================================================
# BEISPIEL: STÄDTENAMEN
# =============================================================================

if __name__ == "__main__":
    
    # Beispieldaten mit allen Problemen:
    cities = [
        # New York - verschiedene Schreibweisen
        'New York',
        'new york',           # Klein
        'NEW YORK',           # GROSS
        'New York City',      # Zusätzliche Info
        'New York, NY',       # Mit Staat
        'NY',                 # Abkürzung
        'downtown New York',  # Irrelevante Info
        
        # Boston - Variationen
        'Boston',
        'boston',             # Klein
        'BOSTON',             # GROSS
        'Boston MA',          # Mit Staat
        'Boston, MA',         # Mit Komma
        'Bos',                # Abkürzung
        
        # Chicago - verschiedene Formate
        'Chicago',
        'chicago',
        'CHICAGO',
        'Chicago IL',
        'Chicago, Illinois',  # Ausgeschrieben
        'Chicgo',             # Tippfehler
        
        # Los Angeles - viele Varianten
        'Los Angeles',
        'los angeles',
        'LOS ANGELES',
        'Los Angeles CA',
        'Los Angeles, California',
        'LA',                 # Abkürzung
        'L.A.',               # Mit Punkten
        'Angeles Los',        # Falsche Reihenfolge
        
        # Miami
        'Miami',
        'miami',
        'MIAMI',
        'Miami FL',
        'Miami, Florida',
        'Miomi',              # Tippfehler

    ]
    
    
    # Bereinigung
    cleaned, mapping = clean_categorical_data(
        cities,
        preference=-0.15,     # Aggressiver für mehr Clustering
        min_similarity=0.4    # Relativ tolerant
    )
    
    
    # Zeige Mapping
    print("\n" + "=" * 70)
    print("MAPPING (Original → Bereinigt)")
    print("=" * 70)
    for original, clean in sorted(set(mapping.items())):
        if original != clean:
            print(f"{original:<30} → {clean}")
    
    # Zeige finale Cluster
    print("\n" + "=" * 70)
    print("FINALE CLUSTER")
    print("=" * 70)
    for i, cluster in enumerate(sorted(set(cleaned)), 1):
        count = cleaned.count(cluster)
        print(f"{i}. '{cluster}' ({count} Einträge)")

    
