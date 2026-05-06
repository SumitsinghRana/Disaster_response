# app/utils/map_utils.py

INDIA_COORDS = {
    # States (approximate center)
    "Uttar Pradesh": [26.8467, 80.9462],
    "Bihar": [25.0961, 85.3131],
    "Rajasthan": [27.0238, 74.2179],
    "Gujarat": [22.2587, 71.1924],
    "Maharashtra": [19.7515, 75.7139],

    # Major cities
    "Delhi": [28.6139, 77.2090],
    "Mumbai": [19.0760, 72.8777],
    "Lucknow": [26.8467, 80.9462],
    "Agra": [27.1767, 78.0081],
    "Varanasi": [25.3176, 82.9739],
    "Meerut": [28.9845, 77.7064],
    "Prayagraj": [25.4358, 81.8463],
    "Allahabad": [25.4358, 81.8463],
    "Kanpur": [26.4499, 80.3319],

    # UP Districts (most relevant for your region)
    "Aligarh": [27.8974, 78.0880],
    "Mathura": [27.4924, 77.6737],
    "Bareilly": [28.3670, 79.4304],
    "Moradabad": [28.8386, 78.7733],
    "Saharanpur": [29.9680, 77.5552],
    "Gorakhpur": [26.7606, 83.3732],
    "Ghaziabad": [28.6692, 77.4538],
    "Noida": [28.5355, 77.3910],
    "Muzaffarnagar": [29.4727, 77.7085],
    "Rampur": [28.8159, 79.0255],
    "Budaun": [28.0390, 79.1128],
    "Sitapur": [27.5693, 80.6832],
    "Lakhimpur": [27.9497, 80.7814],
    "Hardoi": [27.3968, 80.1270],
    "Unnao": [26.5457, 80.4896],
    "Fatehpur": [25.9302, 80.8147],
    "Jaunpur": [25.7465, 82.6836],
    "Azamgarh": [26.0679, 83.1835],
    "Ballia": [25.7554, 84.1490],
    "Ghazipur": [25.5840, 83.5799],
    "Banda": [25.4757, 80.3353],
    "Hamirpur": [25.9570, 80.1517],
    "Etah": [27.5614, 78.6634],
    "Hathras": [27.6059, 78.0528],
    "Kasganj": [27.8073, 78.6407],
    "Sambhal": [28.5902, 78.5691],
    "Amroha": [28.9046, 78.4678],
    "Pilibhit": [28.6312, 79.8051],

    "Almora": [29.5892, 79.6469],
    "Bageshwar": [29.8407, 79.7694],
    "Chamoli": [30.4030, 79.3235],
    "Champawat": [29.3364, 80.0910],
    "Dehradun": [30.3165, 78.0322],
    "Haridwar": [29.9457, 78.1642],
    "Nainital": [29.3919, 79.4542],
    "Pauri Garhwal": [30.1466, 78.7747],
    "Pithoragarh": [29.5820, 80.2182],
    "Rudraprayag": [30.2844, 78.9819],
    "Tehri Garhwal": [30.3786, 78.4800],
    "Udham Singh Nagar": [28.9695, 79.3950],
    "Uttarkashi": [30.7268, 78.4350]
}


def generate_map(locations, urgency_style):
    import folium
    import os

    color_map = {'danger': 'red', 'warning': 'orange', 'success': 'green'}
    color = color_map.get(urgency_style, 'blue')

    m = folium.Map(location=[26.8467, 80.9462], zoom_start=6)

    placed = False
    for loc in locations:
        # Try exact match first, then case-insensitive
        coords = INDIA_COORDS.get(loc) or INDIA_COORDS.get(loc.title())
        if coords:
            folium.Marker(
                location=coords,
                popup=f"<b>{loc}</b>",
                icon=folium.Icon(color=color, icon='exclamation-sign')
            ).add_to(m)
            placed = True

    if not placed and locations:
        # Locations were found in text but we have no coords → show a note
        folium.Marker(
            location=[26.8467, 80.9462],
            popup=f"Approximate: {', '.join(locations)}",
            icon=folium.Icon(color='gray')
        ).add_to(m)

    map_path = os.path.join('templates', 'map.html')
    m.save(map_path)
