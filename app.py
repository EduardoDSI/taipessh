from flask import Flask, send_file
from flask_cors import CORS
import paramiko
from io import BytesIO

app = Flask(__name__)
CORS(app)

@app.route('/descargar_archivo')
def descargar_excel():
    servidor = "ssh-natureza.alwaysdata.net"
    usuario = "natureza_anon"
    password = "(123456)"
    ruta_remota = "taipe.xlsx"

    print("Conectando al servidor para descargar el archivo...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(servidor, username=usuario, password=password, port=22)

    sftp = ssh.open_sftp()

    with sftp.open(ruta_remota, 'rb') as archivo_remoto:
        archivo_buffer = BytesIO(archivo_remoto.read())

    sftp.close()
    ssh.close()

    archivo_buffer.seek(0)
    return send_file(
        archivo_buffer,
        as_attachment=True,
        download_name="taipe.xlsx",
        mimetype=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
