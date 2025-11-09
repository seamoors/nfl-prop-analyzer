"""
NFL Player Prop Analyzer - Flask Web Application
Save this as: app.py
"""

from flask import Flask, render_template_string, jsonify
from datetime import datetime

app = Flask(__name__)

# All the prop data
PROPS_DATA = [
    {'player_name': 'Justin Herbert', 'stat_type': 'Passing Yards', 'line_score': 259.5, 'average': 265.6, 'team': 'LAC'},
    {'player_name': 'Justin Herbert', 'stat_type': 'Pass Completions', 'line_score': 24.5, 'average': 27.1, 'team': 'LAC'},
    {'player_name': 'Ladd McConkey', 'stat_type': 'Receiving Yards', 'line_score': 56.5, 'average': 58.2, 'team': 'LAC'},
    {'player_name': 'Ladd McConkey', 'stat_type': 'Receptions', 'line_score': 4.5, 'average': 5.2, 'team': 'LAC'},
    {'player_name': 'Quentin Johnston', 'stat_type': 'Receiving Yards', 'line_score': 52.5, 'average': 65.7, 'team': 'LAC'},
    {'player_name': 'Kimani Vidal', 'stat_type': 'Rushing Yards', 'line_score': 42.5, 'average': 51.8, 'team': 'LAC'},
    {'player_name': 'Aaron Rodgers', 'stat_type': 'Passing Yards', 'line_score': 215.5, 'average': 211.5, 'team': 'PIT'},
    {'player_name': 'Aaron Rodgers', 'stat_type': 'Pass Completions', 'line_score': 20.5, 'average': 23.2, 'team': 'PIT'},
    {'player_name': 'DK Metcalf', 'stat_type': 'Receiving Yards', 'line_score': 49.5, 'average': 58.4, 'team': 'PIT'},
    {'player_name': 'DK Metcalf', 'stat_type': 'Receptions', 'line_score': 3.5, 'average': 3.6, 'team': 'PIT'},
    {'player_name': 'Jaylen Warren', 'stat_type': 'Rushing Yards', 'line_score': 48.5, 'average': 57.7, 'team': 'PIT'},
    {'player_name': 'Jaylen Warren', 'stat_type': 'Receiving Yards', 'line_score': 22.5, 'average': 27.6, 'team': 'PIT'},
    {'player_name': 'Oronde Gadsden II', 'stat_type': 'Receiving Yards', 'line_score': 52.5, 'average': 58.0, 'team': 'PIT'},
]

HTML = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NFL Prop Analyzer</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
       background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
.container { max-width: 1400px; margin: 0 auto; background: white; border-radius: 20px; 
             box-shadow: 0 20px 60px rgba(0,0,0,0.3); overflow: hidden; }
.header { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 40px; text-align: center; }
.header h1 { font-size: 2.5em; margin-bottom: 10px; }
.content { padding: 40px; }
.section { margin-bottom: 40px; }
.section h3 { color: #2a5298; font-size: 1.6em; margin-bottom: 20px; border-bottom: 3px solid #667eea; padding-bottom: 10px; }
table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
        border-radius: 10px; overflow: hidden; }
thead { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
th { padding: 15px; text-align: left; font-weight: 600; text-transform: uppercase; font-size: 0.85em; }
td { padding: 15px; border-bottom: 1px solid #e9ecef; }
tbody tr:hover { background: #f8f9fa; }
.parlay-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; 
               padding: 30px; border-radius: 15px; margin-bottom: 30px; }
.leg { background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-bottom: 15px; }
.payout-box { background: rgba(255,255,255,0.2); padding: 20px; border-radius: 10px; margin-top: 20px; }
.payout-highlight { font-size: 1.4em; font-weight: bold; color: #ffd700; margin-top: 15px; 
                    padding-top: 15px; border-top: 2px solid rgba(255,255,255,0.3); }
.btn { background: #28a745; color: white; border: none; padding: 15px 30px; border-radius: 25px; 
       font-size: 1.1em; font-weight: 600; cursor: pointer; }
</style>
</head><body>
<div class="container">
<div class="header">
<h1>🏈 NFL Prop Parlay Analyzer</h1>
<p>Conservative 6-Leg Parlays with 10x+ Payout</p>
<p style="margin-top:10px;">Pittsburgh Steelers @ LA Chargers | Monday 8:20 PM ET</p>
</div>
<div class="content">
<div class="section"><h3>📊 All Props ({{total_props}} total)</h3>
<table><thead><tr><th>#</th><th>Player</th><th>Stat</th><th>Line</th><th>Avg</th><th>Cushion</th><th>Confidence</th></tr></thead>
<tbody>{% for p in props %}<tr><td>{{loop.index}}</td><td><strong>{{p.player_name}}</strong></td>
<td>{{p.stat_type}}</td><td>{{p.line_score}}</td><td>{{p.average}}</td>
<td>+{{p.cushion|round(1)}} ({{p.cushion_pct|round(1)}}%)</td><td>{{p.confidence}}</td></tr>{% endfor %}
</tbody></table></div>
<div class="section"><h3>🎫 Main 6-Leg Parlay</h3>
<div class="parlay-card"><h4 style="font-size:1.5em; margin-bottom:20px;">💎 MAIN PARLAY - 6 Legs</h4>
{% for leg in parlay %}<div class="leg"><strong>Leg {{loop.index}}: {{leg.player_name}} ({{leg.team}})</strong><br>
📈 {{leg.stat_type}} OVER {{leg.line_score}}<br>
Season Avg: {{leg.average}} | Cushion: +{{leg.cushion|round(1)}} ({{leg.cushion_pct|round(1)}}%)<br>
Confidence: {{leg.confidence}}</div>{% endfor %}
<div class="payout-box"><h5 style="font-size:1.3em; margin-bottom:15px;">💰 Estimated Payout</h5>
<p>Odds per leg: {{payout.avg_odds_per_leg}}</p>
<p>Combined odds: {{payout.american|round(0)|int}}</p>
<p>Multiplier: {{payout.decimal|round(2)}}x</p>
<div class="payout-highlight">💵 $100 → ${{payout.payout_per_100|round(2)}} 
(Profit: ${{payout.profit_per_100|round(2)}})</div>
{% if payout.decimal >= 10 %}<div style="text-align:center; margin-top:20px; font-size:1.3em;">
✅ 10X+ PAYOUT ACHIEVED! 🎯</div>{% endif %}
</div></div></div>
<div class="section" style="text-align:center;">
<button class="btn" onclick="alert('Copy table data to Excel or use screenshot!')">📥 Export</button>
</div></div></div>
</body></html>'''

def calc_cushion(props):
    result = []
    for p in props:
        cushion = p['average'] - p['line_score']
        cushion_pct = (cushion / p['line_score'] * 100) if p['line_score'] > 0 else 0
        conf = 'VERY HIGH' if cushion_pct >= 30 else 'HIGH' if cushion_pct >= 20 else 'MEDIUM' if cushion_pct >= 10 else 'LOW' if cushion_pct >= 5 else 'RISKY'
        result.append({**p, 'cushion': cushion, 'cushion_pct': cushion_pct, 'confidence': conf})
    return sorted(result, key=lambda x: x['cushion_pct'], reverse=True)

def build_parlay(props):
    good = [p for p in props if p['cushion_pct'] >= 5]
    if len(good) < 6: good = props
    selected, used = [], set()
    for p in good:
        if len(selected) >= 6: break
        if p['player_name'] not in used:
            selected.append(p)
            used.add(p['player_name'])
    for p in good:
        if len(selected) >= 6: break
        if p not in selected: selected.append(p)
    return selected[:6]

def calc_payout(legs, odds=-180):
    decimal = (100 / abs(odds)) + 1
    total = decimal ** legs
    american = (total - 1) * 100 if total >= 2 else -100 / (total - 1)
    return {'legs': legs, 'avg_odds_per_leg': odds, 'decimal': total, 'american': american,
            'payout_per_100': total * 100, 'profit_per_100': (total - 1) * 100}

@app.route('/')
def index():
    props = calc_cushion(PROPS_DATA)
    parlay = build_parlay(props)
    payout = calc_payout(len(parlay))
    return render_template_string(HTML, props=props, total_props=len(props), parlay=parlay, payout=payout)

@app.route('/api')
def api():
    props = calc_cushion(PROPS_DATA)
    parlay = build_parlay(props)
    return jsonify({'props': props, 'parlay': parlay, 'payout': calc_payout(len(parlay))})

if __name__ == '__main__':
    print("🏈 NFL PROP ANALYZER")
    print("="*50)
    print("🚀 Server starting...")
    print("📱 Open: http://localhost:5000")
    print("⭐ Press Ctrl+C to stop")
    print("="*50)
    app.run(debug=True, host='0.0.0.0', port=5000)