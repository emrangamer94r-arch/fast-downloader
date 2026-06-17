from flask import Flask, render_template_string, request, jsonify
import yt_dlp

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Fast Downloader</title>
    <style>
        body { background: #0f172a; color: white; text-align: center; padding: 50px; font-family: sans-serif; }
        input { padding: 10px; width: 80%; border-radius: 5px; border: none; }
        button { padding: 10px 20px; background: #0284c7; color: white; border: none; cursor: pointer; border-radius: 5px; margin-top: 10px; }
        .download-btn { display: block; margin: 20px auto; padding: 10px 20px; background: #22c55e; color: white; text-decoration: none; width: 200px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>⚡ Fast Video Downloader</h1>
    <input type="text" id="url" placeholder="ভিডিও লিংক দিন...">
    <br><button onclick="download()">লিংক তৈরি করুন</button>
    <div id="result"></div>
    <script>
    function download() {
        let url = document.getElementById('url').value;
        fetch('/download', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({url: url})})
        .then(res => res.json()).then(data => {
            if(data.url) document.getElementById('result').innerHTML = `<a href="${data.url}" class="download-btn" target="_blank">📥 ডাউনলোড করুন</a>`;
            else alert('লিংক কাজ করছে না!');
        });
    }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_TEMPLATE)

@app.route('/download', methods=['POST'])
def download():
    url = request.get_json().get('url')
    try:
        ydl_opts = {'format': 'best', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({'url': info.get('url')})
    except: return jsonify({'success': False})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000)
