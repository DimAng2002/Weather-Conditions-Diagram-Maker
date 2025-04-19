import os
import re
from datetime import date, datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def create_excel_charts(all_region_data):
    import xlsxwriter
    
    # Δημιουργία του Excel αρχείου
    workbook = xlsxwriter.Workbook('Temperature_Analysis.xlsx')
    
    # Για κάθε περιοχή
    for region_name, region_data in all_region_data.items():
        # Οργάνωση δεδομένων ανά έτος
        years_data = {}
        
        for data in region_data:
            if 'year' in data and 'month' in data and 'temperature' in data:
                year = data['year']
                if year not in years_data:
                    years_data[year] = []
                
                month_clean = data['month'].split()[0]
                try:
                    month_num = int(month_clean)
                    temp = float(data['temperature']) if isinstance(data['temperature'], str) else data['temperature']
                    years_data[year].append((month_num, temp))
                except (ValueError, TypeError):
                    continue
        
        # Για κάθε έτος
        for year, year_data in years_data.items():
            # Ταξινόμηση δεδομένων ανά μήνα
            year_data.sort(key=lambda x: x[0])
            
            # Δημιουργία φύλλου εργασίας για αυτή την περιοχή και έτος
            worksheet = workbook.add_worksheet(f"{region_name}_{year}")
            
            # Επικεφαλίδες
            worksheet.write(0, 0, "Μήνας")
            worksheet.write(0, 1, "Θερμοκρασία")
            
            # Δεδομένα
            for row, (month, temp) in enumerate(year_data, start=1):
                worksheet.write(row, 0, month)
                worksheet.write(row, 1, temp)
            
            # Δημιουργία διαγράμματος
            chart = workbook.add_chart({'type': 'line'})
            
            # Προσθήκη σειράς δεδομένων στο διάγραμμα
            chart.add_series({
                'name':       f'Θερμοκρασία {year}',
                'categories': [f"{region_name}_{year}", 1, 0, len(year_data), 0],
                'values':     [f"{region_name}_{year}", 1, 1, len(year_data), 1],
                'marker':     {'type': 'circle', 'size': 8},
                'data_labels': {'value': True},
            })
            
            # Ρύθμιση τίτλων διαγράμματος
            chart.set_title({'name': f'Μέση Θερμοκρασία {region_name} - {year}'})
            chart.set_x_axis({'name': 'Μήνας'})
            chart.set_y_axis({'name': 'Θερμοκρασία (°C)'})
            
            # Εισαγωγή διαγράμματος στο φύλλο εργασίας
            worksheet.insert_chart('D2', chart, {'x_scale': 1.5, 'y_scale': 1})
    
    workbook.close()
    print("Δημιουργήθηκε το αρχείο Excel με τα διαγράμματα: Temperature_Analysis.xlsx")

def takeValues(arxeio):
    with open(arxeio, "r") as file:
        content = file.read()
        temp_pattern = r'--+\n\s+(\d+\.\d+)\s+(\d+\.\d+)'
        temp_match = re.search(temp_pattern, content)
        
        if temp_match:
            avg_temp = float(temp_match.group(1))
            return avg_temp


def create_plot_for_region(region_data, region_name):
    years_data = {}    

    for data in region_data:
        if 'year' in data and 'month' in data and 'temperature' in data:
            year = data['year']
            if year not in years_data:
                years_data[year] = []
            
            month_clean = data['month'].split()[0]
            date_obj = datetime.strptime(f"{year}-{month_clean}", "%Y-%m")
            temp = float(data['temperature']) 
            years_data[year].append((date_obj, temp))
    
    
    for year, year_data in years_data.items():
        dates = []
        temperatures = []
        
        year_data.sort(key=lambda x: x[0])
        
        for date_obj, temp in year_data:
            dates.append(date_obj)
            temperatures.append(temp)


            
        
        plt.figure(figsize=(20, 9))
        plt.plot(dates, temperatures, marker='o', linestyle='-')
        for i, (date_obj, temp) in enumerate(zip(dates, temperatures)):
            plt.annotate(f"{temp:.1f}", (date_obj, temp),textcoords="offset points", xytext=(0, 10), ha='center',fontsize=9)      



        plt.title(f"Μέση θερμοκρασία περιοχής {region_name} - {year}")
        plt.xlabel("Μήνας")
        plt.ylabel("Θερμοκρασία (°C)")
        plt.grid(True)
        
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.xticks(rotation=0)
        plt.tight_layout()
        
        plt.savefig(os.path.join(os.path.join("Diagrams",region_name), f"{region_name}_{year}_temperature.png"))
        plt.close()
        print(f"Το διάγραμμα για την περιοχή {region_name} έτους {year} δημιουργήθηκε")

def main():
    perioxes = []
    regionData = {}
    
    for arxeio in os.listdir("Text_Files"):
        if arxeio.endswith(".TXT"):
            region = arxeio.split('-')[0]
            if region not in perioxes:
                perioxes.append(region)
                regionData[region] = []
    
    for perioxi in perioxes:
        print(f"=-=-=-=-=-=-=-=-={perioxi}-=-=-=-=-=-=-=-=-=")
        
        for arxeio in os.listdir("Text_Files"):
            if arxeio.endswith(".TXT") and arxeio.startswith(perioxi):
                parts = arxeio.split('-')
                if len(parts) >= 3:
                    year = parts[1]
                    month = parts[2].split('.')[0]
                    
                    file_path = os.path.join("Text_Files", arxeio)
                    temperature = takeValues(file_path)
                    
                    regionData[perioxi].append({'year': year,'month': month,'temperature': temperature})
        
        if perioxi in regionData:
            if perioxi not in os.listdir("Diagrams"):
                os.mkdir(os.path.join("Diagrams", perioxi))
            create_plot_for_region(regionData[perioxi], perioxi)
    create_excel_charts(regionData)

if __name__ == "__main__":
    main()