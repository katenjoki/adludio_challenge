import sys
sys.path.append('scripts')
from campaign import site_scores
import pandas as pd

out =site_scores('fiwemi8')
z = out.to_html()
print(z)