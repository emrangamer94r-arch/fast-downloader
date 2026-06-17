from flask import Flask, render_template_string, request, jsonify
import yt_dlp

app = Flask(__name__)

# ওয়েবসাইটের ডিজাইন (HTML/CSS)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚡ Free Social Media Video Downloader</title>
    <style>
        body { font-family: 'Arial', sans-serif; background-color: #0f172a; color: white; text-align: center; padding: 20px; }
        .container { max-width: 600px; margin: 50px auto; background: #1e293b; padding: 30px; border-radius: 15px; box-shadow: 0px 4px 15px rgba(0,0,0,0.5); }
        h1 { color: #38bdf8; font-size: 24px; margin-bottom: 10px; }
        p { color: #94a3b8; font-size: 14px; }
        input[type="text"] { width: 90%; padding: 12px; margin: 20px 0; border: none; border-radius: 8px; font-size: 16px; background: #334155; color: white; text-align: center; }
        button { background: #0284c7; color: white; padding: 12px 30px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; transition: 0.3s; font-weight: bold; }
        button:hover { background: #0369a1; }
        #result { margin-top: 25px; padding: 15px; border-radius: 8px; background: #0f172a; display: none; }
        .download-btn { display: inline-block; background: #22c55e; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 10px; }
        .download-btn:hover { background: #16a34a; }
        .tg-banner { margin-top: 30px; padding: 15px; background: #0284c7; border-radius: 8px; font-weight: bold; }
        .tg-banner a { color: #fff; text-decoration: underline; }
    </style>
</head>
<body>

<div class="container">
    <h1>⚡ Fast Video Downloader</h1>
    <p>ফেসবুক, ইউটিউব, টিকটক বা ইনস্টাগ্রাম ভিডিওর লিংক নিচে পেস্ট করুন</p>
    
    <input type="text" id="videoUrl" placeholder="এখানে ভিডিওর লিংক দিন...">
    <br>
    <button onclick="getDownloadLink()">ভিডিও লিংক তৈরি করুন</button>
    
    <div id="result">
        <p style="color: #22c55e; font-weight: bold;">আপনার ভিডিও ডাউনলোডের জন্য রেডি! 👇</p>
        <p id="videoTitle" style="font-size: 14px; color: #cbd5e1;"></p>
        <div id="linksContainer"></div>
    </div>
    
    <div class="tg-banner">
        📢 আমাদের অফিশিয়াল টেলিগ্রাম চ্যানেলে জয়েন করুন! <br>
        <a href="https://t.me/bd_trading_king_official" target="_blank">এখানে ক্লিক করে জয়েন করুন</a>
    </div>
</div>

<script>
function getDownloadLink() {
    var url = document.getElementById('videoUrl').value;
    if(!url) { alert('দয়া করে একটি লিংক দিন!'); return; }
    
    var resultDiv = document.getElementById('result');
    var linksContainer = document.getElementById('linksContainer');
    var videoTitle = document.getElementById('videoTitle');
    
    resultDiv.style.display = 'block';
    linksContainer.innerHTML = 'প্রসেসিং হচ্ছে, একটু অপেক্ষা করুন... ⏳';
    videoTitle.innerHTML = '';
    
    fetch('/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url })
    })
    .then(res => res.json())
    .then(data => {
        if(data.success) {
            videoTitle.innerHTML = "🎬 <b>Title:</b> " + data.title;
            linksContainer.innerHTML = `<a href="${data.download_url}" class="download-btn" target="_blank" download>📥 ক্লিক করে ভিডিও ডাউনলোড করুন</a>`;
        } else {
            linksContainer.innerHTML = '<span style="color: #ef4444;">❌ এরর: লিংকটি সাপোর্ট করছে না বা সমস্যা হয়েছে!</span>';
        }
    })
    .catch(err => {
        linksContainer.innerHTML = '<span style="color: #ef4444;">❌ কানেকশন এরর হয়েছে!</span>';
    });
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download', \
methods=['POST'])
def download():
    data = request.get_json()
    video_url = data.get('url')
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_title = info.get('title', 'Social Media Video')
            
            # ডিরেক্ট ইউআরএল বা ফরম্যাট লিস্ট থেকে সেরাটা নেওয়া
            direct_url = info.get('url') or (info.get('formats')[0].get('url') if info.get('formats') else None)
            
            if direct_url:
                return jsonify({'success': True, 'title': video_title, 'download_url': direct_url})
            
            return jsonify({'success': False})
            
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
