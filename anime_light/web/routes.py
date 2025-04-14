import os
from flask import (
    render_template, request, redirect, 
    url_for, send_from_directory, 
    Blueprint, current_app, flash
)
from werkzeug.utils import secure_filename
from anime_light.web.utils import allowed_file

index_bp = Blueprint('index', __name__, template_folder='templates')

@index_bp.route('/')
def index():
    return render_template('index.html')

@index_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No se seleccionó ningún archivo', 'error')
        return redirect(url_for('index.index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('Nombre de archivo vacío', 'error')
        return redirect(url_for('index.index'))
    
    if not allowed_file(file.filename):
        flash('Formato de archivo no permitido', 'error')
        return redirect(url_for('index.index'))
    
    try:
        filename = secure_filename(file.filename)
        input_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        output_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"converted_{filename}")
        
        file.save(input_path)
        
        # TODO: Aquí iría tu lógica de conversión con FFmpeg
        # subprocess.run(['ffmpeg', '-i', input_path, ...])
        
        flash('¡Archivo convertido con éxito!', 'success')
        return redirect(url_for('index.download', filename=f"converted_{filename}"))
    
    except Exception as e:
        current_app.logger.error(f"Error al procesar el archivo: {e}")
        flash('Error interno al procesar el archivo', 'error')
        return redirect(url_for('index.index'))

@index_bp.route('/download/<filename>')
def download(filename):
    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'], 
        filename, 
        as_attachment=True
    )