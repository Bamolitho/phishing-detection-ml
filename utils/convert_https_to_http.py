import pandas as pd
from utils.find_path import get_data_path

def convert_https_to_http(input_excel, output_csv):
    # Lire le fichier Excel
    df = pd.read_excel(input_excel)

    # Vérifier les colonnes nécessaires
    if 'url' not in df.columns or 'type' not in df.columns:
        raise ValueError("Le fichier doit contenir deux colonnes : 'url' et 'type'.")

    # Remplacer https:// par http:// dans la colonne 'url'
    df['url'] = df['url'].str.replace('^https://', 'http://', regex=True)

    # Sauvegarder en CSV avec les deux colonnes conservées
    df[['url', 'type']].to_csv(output_csv, index=False)
    print(f"✅ Fichier converti enregistré : {output_csv}")

# Exemple d’utilisation
if __name__ == "__main__":
    input_file = get_data_path("url_dataset.xlsx")
    output_file = get_data_path("http_url_dataset.csv")
    convert_https_to_http(input_file, output_file)
