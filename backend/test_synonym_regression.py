import re

syn_set = {"bachelor", "b.s.", "bs", "bachelors", "undergraduate"}
s_lower = "bachelor of arts in english"
t_lower = "bachelor's degree in computer science"

def boundary_match(word, text):
    boundary_start = r"(?:^|[^\w+#])"
    boundary_end = r"(?:$|[^\w+#])"
    pattern = boundary_start + re.escape(word) + boundary_end
    return bool(re.search(pattern, text))

s_match = any(boundary_match(w, s_lower) for w in syn_set)
t_match = any(boundary_match(w, t_lower) for w in syn_set)

print(f"s_match: {s_match}")
print(f"t_match: {t_match}")
if s_match and t_match:
    print("Regression: It matches! English degree matched to CS requirement just because both have 'bachelor'!")
