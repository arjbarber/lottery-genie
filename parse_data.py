import csv
import sqlite3

def csv_to_sqlite(csvfile, dbfile, table_name):
    db = sqlite3.connect(dbfile)
    cursor = db.cursor()

    with open(csvfile, 'r') as file:
        reader = csv.reader(file)
        
        columns = next(reader)
        columns = [column.strip() for column in columns]

        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})")

        for row in reader:
            placeholders = ', '.join(['?'] * len(row))
            cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", row)

    db.commit()
    db.close()

def parse_numbers(csvfile, modifiedcsvfile):
    with open(csvfile, 'r') as infile, open(modifiedcsvfile, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['n1', 'n2', 'n3', 'n4', 'n5']
        fieldnames.remove("Winning Numbers")
        fieldnames.remove("Multiplier")
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in reader:
            winning_numbers = row["Winning Numbers"].split()
            row.update({
                'n1': winning_numbers[0],
                'n2': winning_numbers[1],
                'n3': winning_numbers[2],
                'n4': winning_numbers[3],
                'n5': winning_numbers[4],
            })
            row.pop("Winning Numbers")
            row.pop("Multiplier")
            writer.writerow(row)

def parse_dates(csvfile, modifiedcsvfile):
    with open(csvfile, 'r') as infile, open(modifiedcsvfile, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["month", "day", "year"]
        fieldnames.remove("Draw Date")
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in reader:
            dates = row["Draw Date"].split("/")
            row.update({
                'month': dates[0],
                'day': dates[1],
                'year': dates[2]
            })
            row.pop("Draw Date")
            writer.writerow(row)

def main():
    csvfile = 'Lottery_Mega_Millions_Winning_Numbers__Beginning_2002_20240806.csv'
    modifiedcsvfiledates = "Modified Dates: " + csvfile
    modifiedcsvfilenumbers = "Modified Nos: " + csvfile
    modifiedcsvfilemultiplier = "Deleted Multiplier: " + csvfile
    dbfile = 'data.db'
    table_name = 'numbers'

    parse_dates(csvfile,modifiedcsvfiledates)
    parse_numbers(modifiedcsvfiledates, modifiedcsvfilenumbers)
    csv_to_sqlite(modifiedcsvfilenumbers, dbfile, table_name)

if __name__ == "__main__":
    main()