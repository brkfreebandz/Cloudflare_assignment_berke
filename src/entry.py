from workers import Response, WorkerEntrypoint
import json

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        url = str(request.url)
        path = "/" + url.split("/", 3)[3] if len(url.split("/", 3)) > 3 else "/"
        if "?" in path:
            path = path.split("?")[0]
        
        if path == "/":
            return self.serve_dashboard()
        elif path == "/api/feedback":
            return await self.get_feedback()
        elif path == "/api/stats":
            return await self.get_stats()
        else:
            return Response("Not Found", status=404)
    
    def serve_dashboard(self):
        html = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Feedback Analyzer</title>
<script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-gray-100"><div class="container mx-auto px-4 py-8">
<h1 class="text-4xl font-bold mb-8">📊 Feedback Analyzer</h1>
<div class="grid grid-cols-3 gap-4 mb-8">
<div class="bg-white rounded-lg shadow p-6"><h3 class="text-gray-500 text-sm mb-2">Total</h3>
<p id="total-count" class="text-3xl font-bold">-</p></div>
<div class="bg-white rounded-lg shadow p-6"><h3 class="text-gray-500 text-sm mb-2">Sentiment</h3>
<div id="sentiment-stats">Loading...</div></div>
<div class="bg-white rounded-lg shadow p-6"><h3 class="text-gray-500 text-sm mb-2">Categories</h3>
<div id="category-stats">Loading...</div></div></div>
<div class="bg-white rounded-lg shadow"><div class="px-6 py-4 border-b">
<h2 class="text-xl font-semibold">Recent Feedback</h2></div>
<table class="min-w-full"><thead class="bg-gray-50"><tr>
<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Source</th>
<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Content</th>
<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Sentiment</th>
<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Category</th>
</tr></thead><tbody id="feedback-table">
<tr><td colspan="4" class="px-6 py-4 text-center">Loading...</td></tr></tbody></table></div></div>
<script>
async function loadData() {
const f = await fetch('/api/feedback'); const feedback = await f.json();
const s = await fetch('/api/stats'); const stats = await s.json();
document.getElementById('total-count').textContent = feedback.length;
const sh = Object.entries(stats.sentiment||{}).map(([k,v])=>'<div class="flex justify-between"><span>'+k+'</span><span class="font-bold">'+v+'</span></div>').join('');
document.getElementById('sentiment-stats').innerHTML = sh;
const ch = Object.entries(stats.category||{}).map(([k,v])=>'<div class="flex justify-between"><span>'+k+'</span><span class="font-bold">'+v+'</span></div>').join('');
document.getElementById('category-stats').innerHTML = ch;
const c = {positive:'bg-green-100 text-green-800',negative:'bg-red-100 text-red-800',neutral:'bg-yellow-100 text-yellow-800'};
const th = feedback.map(i=>'<tr><td class="px-6 py-4"><span class="px-2 py-1 text-xs rounded bg-blue-100">'+i.source+'</span></td><td class="px-6 py-4">'+i.content+'</td><td class="px-6 py-4"><span class="px-2 py-1 text-xs rounded '+c[i.sentiment]+'">'+i.sentiment+'</span></td><td class="px-6 py-4">'+i.category+'</td></tr>').join('');
document.getElementById('feedback-table').innerHTML = th;
}
loadData();
</script></body></html>"""
        return Response(html, headers={"Content-Type": "text/html"})
    
    async def get_feedback(self):
        try:
            stmt = self.env.feedback_db.prepare("SELECT * FROM feedback ORDER BY created_at DESC")
            result = await stmt.all()
            
            # Convert JS proxy to Python - access results directly as JSON-compatible
            data = result.results.to_py()
            
            return Response(json.dumps(data), headers={"Content-Type": "application/json"})
        except Exception as e:
            return Response(json.dumps({"error": str(e)}), status=500, headers={"Content-Type": "application/json"})
    
    async def get_stats(self):
        try:
            stmt1 = self.env.feedback_db.prepare("SELECT sentiment, COUNT(*) as count FROM feedback GROUP BY sentiment")
            r1 = await stmt1.all()
            stmt2 = self.env.feedback_db.prepare("SELECT category, COUNT(*) as count FROM feedback GROUP BY category")
            r2 = await stmt2.all()
            
            # Convert to Python
            sentiment_data = r1.results.to_py()
            category_data = r2.results.to_py()
            
            sentiment_dict = {row["sentiment"]: row["count"] for row in sentiment_data}
            category_dict = {row["category"]: row["count"] for row in category_data}
            
            stats = {"sentiment": sentiment_dict, "category": category_dict}
            return Response(json.dumps(stats), headers={"Content-Type": "application/json"})
        except Exception as e:
            return Response(json.dumps({"error": str(e)}), status=500, headers={"Content-Type": "application/json"})
