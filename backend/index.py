# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# # from upload import sftp_upload
# from sftp import sftp_download, sftp_upload, sftp_remove, sftp_listdir
# from sftp import getFiles

# app = Flask(__name__)
# CORS(app)  # CORS'u etkinleştir

# UPLOAD_FOLDER = 'uploads'  # uploads klasörü çalışma dizininde oluşturulacak
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'})
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'})
#     if file and allowed_file(file.filename):
#         filename = file.filename
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)
#         # sftp_upload(filepath, filename)  # Dosya yolunu geçiyoruz
#         sftp_upload('192.168.207.166','buraxta','buraxta', filepath, filename)
#         return jsonify({'success': 'File successfully uploaded'})
#     return jsonify({'error': 'File not allowed'})

# @app.route('/getfiles', methods=['GET'])
# def get_files():
#     files = getFiles()
#     return jsonify({'files': files})

# @app.route('/download', methods=['POST'])
# def download_file():
#     data = request.json
#     file_id = data.get('id')
    
#     if file_id is None:
#         return jsonify({'error': 'No file id provided'})

#     files = getFiles()
    
#     try:
#         file_id = int(file_id)
#         if file_id < 0 or file_id >= len(files):
#             return jsonify({'error': 'Invalid file id'})
#     except ValueError:
#         return jsonify({'error': 'File id must be an integer'})

#     file_name = files[file_id]
#     remote_path = f"/home/buraxta/uploads/{file_name}"
#     local_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    
#     # SFTP ile dosyayı uzak sunucudan indir
#     downloaded_file = sftp_download('192.168.207.166', 'buraxta', 'buraxta', remote_path, local_path)
    
#     if downloaded_file:
#         return send_file(downloaded_file, as_attachment=True)
#     else:
#         return jsonify({'error': 'Failed to download file'})

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
# from upload import sftp_upload
from sftp import sftp_download, sftp_upload, sftp_remove, sftp_listdir
from sftp import getFiles

app = Flask(__name__)
CORS(app)  # CORS'u etkinleştir

UPLOAD_FOLDER = 'uploads'  # uploads klasörü çalışma dizininde oluşturulacak
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file and allowed_file(file.filename):
        filename = file.filename
        print(filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # sftp_upload(filepath, filename)  # Dosya yolunu geçiyoruz
        sftp_upload('192.168.207.166','buraxta','buraxta', filepath, f"/home/buraxta/Desktop/sample/{filename}")
        return jsonify({'success': 'File successfully uploaded'})
    return jsonify({'error': 'File not allowed'})

@app.route('/getfiles', methods=['GET'])
def get_files():
    files = getFiles()
    return jsonify({'files': files})

@app.route('/download', methods=['POST'])
def download_file():
    data = request.json
    file_id = data.get('id')
    
    if file_id is None:
        return jsonify({'error': 'No file id provided'})

    files = getFiles()
    
    try:
        file_id = int(file_id)
        if file_id < 0 or file_id >= len(files):
            return jsonify({'error': 'Invalid file id'})
    except ValueError:
        return jsonify({'error': 'File id must be an integer'})

    file_name = files[file_id]
    remote_path = f"/home/buraxta/Desktop/sample/{file_name}"
    local_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    
    # SFTP ile dosyayı uzak sunucudan indir
    downloaded_file = sftp_download('192.168.207.166', 'buraxta', 'buraxta', remote_path, local_path)
    
    if downloaded_file and os.path.exists(downloaded_file):
        try:
            return send_file(downloaded_file, as_attachment=True)
        except Exception as e:
            print("Dosya gönderilirken hata oluştu:", e)
            return jsonify({'error': f'Failed to send file: {str(e)}'})
    else:
        return jsonify({'error': 'Failed to download file'})

@app.route('/delete', methods=['POST'])
def delete_file():
    data = request.json
    file_id = data.get('id')
    
    if file_id is None:
        return jsonify({'error': 'No file id provided'})

    files = getFiles()
    
    try:
        file_id = int(file_id)
        if file_id < 0 or file_id >= len(files):
            return jsonify({'error': 'Invalid file id'})
    except ValueError:
        return jsonify({'error': 'File id must be an integer'})

    file_name = files[file_id]
    print(file_name)
    remote_path = f"/home/buraxta/Desktop/sample/{file_name}"
    
    # SFTP ile dosyayı uzak sunucudan sil
    file_deleted = sftp_remove('192.168.207.166', 'buraxta', 'buraxta', remote_path)
    
    if file_deleted:
        return jsonify({'success': 'File deleted successfully'})
    else:
        return jsonify({'error': 'Failed to delete file'})

if __name__ == '__main__':
    app.run(debug=True)

