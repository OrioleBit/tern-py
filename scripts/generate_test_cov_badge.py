import os
import xml.etree.ElementTree as ET

print("Current dir:", os.getcwd())
print("Files:", os.listdir())
os.makedirs("docs", exist_ok=True)

tree = ET.parse("coverage.xml")
root = tree.getroot()
percent = float(root.attrib["line-rate"]) * 100

with open("docs/coverage_badge.svg", "w") as f:
    f.write(f"""
<svg xmlns="http://www.w3.org/2000/svg" width="120" height="20">
  <rect width="120" height="20" fill="#555"/>
  <rect x="60" width="60" height="20" fill="#4c1"/>
  <text x="30" y="14" fill="#fff" font-family="Verdana" font-size="11">coverage</text>
  <text x="90" y="14" fill="#fff" font-family="Verdana" font-size="11">{percent:.0f}%</text>
</svg>
""")

print("Badge generated successfully")
