import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("loscuatesggwp123@gmail.com", "mnzlmtahnhpmgmex")
    print("¡CONEXIÓN EXITOSA! El problema no son las credenciales.")
    server.quit()
except Exception as e:
    print(f"ERROR: {e}")