import pyodbc

try:
    conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=lgallussqlserver.database.windows.net;DATABASE=bddussba;UID=leo;PWD=leflibustierdu59!;Encrypt=yes;TrustServerCertificate=no')
    print('Connexion réussie à la base de données')
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    row = cursor.fetchone()
    print("Version de SQL Server:", row[0])
    conn.close()
except Exception as e:
    print(f'Erreur de connexion: {str(e)}')
