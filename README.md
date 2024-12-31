# Statistika Pro Všechny

## Popis práce
Statistika Pro Všechny je webová aplikace, která poskytuje vizualizaci statistických dat a predikce pomocí strojového učení. Aplikace si klade za cíl zpřístupnit statistická data z Českého statistického úřadu (ČSÚ) širší veřejnosti a učinit je užitečnějšími. Uživatelé mohou procházet data, zobrazovat grafy a získávat predikce budoucích trendů. Projekt kombinuje uživatelsky přívětivé rozhraní s analytickými nástroji, což zvyšuje zájem o data z ČSÚ a podporuje jejich širší využití.

## Popis souborů

### Hlavní adresář
- `manage.py`: Hlavní spouštěcí soubor Django projektu.
- `_README.txt`: Tento soubor obsahující popis projektu a jednotlivých souborů.
- `requirements.txt` Seznam závislostí a balíčků potřebných pro běh projektu. na produkci

### Adresář `spv_project`
- `asgi.py`: Konfigurační soubor pro ASGI server.
- `settings.py`: Konfigurační soubor pro Django projekt.
- `urls.py`: Definice URL tras pro celý projekt.
- `wsgi.py`: Konfigurační soubor pro WSGI server.
- `deployment.py`: Konfigurační soubor pro Django projekt na prdukci.

### Adresář `blog`
- `admin.py`: Konfigurace administrátorského rozhraní pro modely.
- `apps.py`: Konfigurace aplikace `blog`.
- `models.py`: Definice databázových modelů pro články, kategorie a soubory Excel.
- `tests.py`: Testovací soubory pro aplikaci `blog`.
- `urls.py`: Definice URL tras pro aplikaci `blog`.
- `views.py`: Definice pohledů (views) pro aplikaci `blog`.

### Adresář `templates/blog`
- `base.html`: Základní šablona pro všechny stránky.
- `index.html`: Šablona pro domovskou stránku.
- `about.html`: Šablona pro stránku "O nás".
- `article.html`: Šablona pro stránku "O nás".
- `article_list.html`: Šablona pro stránku "O nás".

### Adresář `static/css`
- `styles.css`: Vlastní styly pro aplikaci.

### Adresář `static/images`
- `favicon.png`: Ikona webu.
- `logo.png`: Logo aplikace.



