import os
from flask import Flask, request, redirect, make_response, jsonify, url_for, send_from_directory


app = Flask(__name__)
app.config["image_upload"] = "./img"

allowed_extensions = set(['png', 'jpg', 'jpge']) #Objeto iterable de strings

@app.route("/")
def home():
    return Hola

def allowed_file(filename): 
    """ 
        Se valida que la extención del archivo este dentro de las 
        opciones definidas en allowed_extensions, para su almacenamiento 
        - Retorna True o False
    """
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed_extensions

@app.route("/upload-image", methods = ["GET", "POST"])
def upload_image(): 
    """ 
        Recibe y almacena de las images suminitradas por el user que 
        cumplan con las validaciones establecidas. Se almacenan de forma local
        y no en una bd
        - Si la operación es exitosa, recarga la pagina mostrando la imagen almacenada
        - Si la extencion no es valida, se envia un mensaje 400
    """
    if request.method == "POST": 
        
        if  request.files:
                img = request.files['image']
                filename = img.filename
                
                if allowed_file(filename): 
                    img.save(os.path.join(app.config["image_upload"], filename))
                    return redirect(url_for("get_image", filename=filename))
                
                return make_response(jsonify({ 'error': 'formato u extension de imagen no soportado'}), 400)
            
        return make_response(jsonify({'error': 'no se envio un archivo o nomenclatura de formato erronea'}), 400)
            
    return """ 
                <form method="POST" enctype="multipart/form-data">
                    <input type= "file" name="image">
                    <button type="submit">Enviar</button>
                </form>
            """
            
@app.route("/upload-image/<filename>")
def get_image(filename):
    """  
        Busca en el dir configurado el archivo que concuerde con el nombre 
        suministrada como parametro de entrada. Si el archivo esta almacenado,
        es renderizado en el navegador
    """
    return   send_from_directory(app.config["image_upload"], filename)
 
 
if __name__ == "__main__": 
    app.run(debug= True)
