from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h2>YouTube Downloader</h2>
    <form action="/download" method="post">
        <input name="url" placeholder="YouTube URL" required><br><br>
        <select name="format">
            <option value="mp4">MP4</option>
            <option value="mp3">MP3</option>
        </select><br><br>
        <button type="submit">Download</button>
    </form>
    '''

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    fmt = request.form['format']

    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s'
    }

    if fmt == 'mp3':
        ydl_opts.update({
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        ydl_opts['format'] = 'bestvideo+bestaudio/best'

    os.makedirs('downloads', exist_ok=True)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        if fmt == 'mp3':
            filename = filename.replace('.webm', '.mp3')

    return send_file(filename, as_attachment=True)
