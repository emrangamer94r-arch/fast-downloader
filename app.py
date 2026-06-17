from flask import Flask, render_template_string, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
    <body style="background:#000; color:#fff; text-align:center; padding:50px;">
    <h1>Video Downloader</h1>
    <input type="text" id="u" style="width:80%; padding:10px;">
    <button onclick="d()" style="padding:10px;">Get Link</button>
    <div id="r"></div>
    <script>
    function d(){
        let url = document.getElementById('u').value;
        fetch('/dl', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({url:url})})
        .then(res=>res.json()).then(data=>{
            if(data.url) document.getElementById('r').innerHTML = '<a href="'+data.url+'" style="color:lime;">Download Now</a>';
            else alert('Error: Please try another video or check link.');
        });
    }
    </script>
    </body>
    ''')

@app.route('/dl', methods=['POST'])
def dl():
    url = request.get_json().get('url')
    try:
        # এখানে আমরা হেডার এবং বাইপাস সেটিংস যুক্ত করছি
        ydl_opts = {
            'format': 'best',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'geo_bypass': True,
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({'url': info.get('url')})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000)
